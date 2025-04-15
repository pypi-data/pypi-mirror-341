import { useEffect, useRef, useMemo } from 'react';
import {genstudio} from './globals'
interface CanvasRegistry {
  [key: string]: {
    canvas: HTMLCanvasElement;
    overlay?: HTMLImageElement;
    device?: GPUDevice;
    context?: GPUCanvasContext;
    renderCallback?: (texture: GPUTexture, depthTexture: GPUTexture | null) => void;
  };
}

// Global registry of active canvases
const activeCanvases: CanvasRegistry = {};

/**
 * Hook to register a canvas element for snapshot functionality
 * @param id Unique identifier for the canvas
 * @param device Optional WebGPU device to use for texture copying
 * @param context Optional WebGPU context for rendering
 * @param renderCallback Optional callback to render the scene to a texture
 * @returns Object containing the ref to attach to canvas and snapshot management functions
 */
export function useCanvasSnapshot(
  device?: GPUDevice,
  context?: GPUCanvasContext,
  renderCallback?: (texture: GPUTexture, depthTexture: GPUTexture | null) => void
) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const id = useMemo(() => `scene3d_${Math.random().toString(36).slice(2)}`, []);

  useEffect(() => {
    if (canvasRef.current) {
      // Register canvas when mounted
      activeCanvases[id] = {
        canvas: canvasRef.current,
        device,
        context,
        renderCallback
      };

      // Cleanup on unmount
      return () => {
        delete activeCanvases[id];
      };
    }
  }, [id, device, context, renderCallback]);

  return {
    canvasRef,
    getActiveCanvases: () => Object.keys(activeCanvases)
  };
}

/**
 * Creates image overlays for all registered WebGPU canvases
 * Used before PDF export to capture 3D content as static images
 *
 * @returns Promise that resolves when all overlays are created
 * @throws May throw if WebGPU operations fail
 */
export async function createCanvasOverlays(): Promise<void> {
  await Promise.all(
    Object.entries(activeCanvases).map(async ([id, entry]) => {
      const { canvas, device, context, renderCallback } = entry;
      if (!device || !context || !renderCallback) {
        console.warn(`[canvasSnapshot] Missing required WebGPU resources for canvas ${id}`);
        return;
      }

      console.log("[canvasSnapshot] Starting overlay creation for canvas:", id);

      // Get canvas dimensions
      const width = canvas.width;
      const height = canvas.height;

      // Calculate aligned bytes per row (must be multiple of 256)
      const bytesPerPixel = 4; // RGBA8
      const bytesPerRow = Math.ceil((width * bytesPerPixel) / 256) * 256;
      const alignedBufferSize = bytesPerRow * height;

      // Create a texture to render the scene to
      const texture = device.createTexture({
        size: [width, height],
        format: navigator.gpu.getPreferredCanvasFormat(),
        usage: GPUTextureUsage.COPY_SRC | GPUTextureUsage.RENDER_ATTACHMENT
      });

      // Create a depth texture for the render pass
      const depthTexture = device.createTexture({
        size: [width, height],
        format: 'depth24plus',
        usage: GPUTextureUsage.RENDER_ATTACHMENT
      });

      // Render the scene to our texture
      renderCallback(texture, depthTexture);

      // Create a buffer to read back the pixel data
      const readbackBuffer = device.createBuffer({
        size: alignedBufferSize,
        usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ
      });

      // Copy from our texture to the buffer
      const commandEncoder = device.createCommandEncoder();
      commandEncoder.copyTextureToBuffer(
        { texture },
        {
          buffer: readbackBuffer,
          bytesPerRow,
          rowsPerImage: height
        },
        [width, height, 1]
      );
      device.queue.submit([commandEncoder.finish()]);

      // Wait for the copy to complete and map the buffer
      await readbackBuffer.mapAsync(GPUMapMode.READ);
      const mappedData = new Uint8Array(readbackBuffer.getMappedRange());

      // Create a properly sized array for the actual pixel data
      const pixelData = new Uint8Array(width * height * bytesPerPixel);

      // Create Uint32Array views of both buffers for faster processing
      // Need to account for the aligned buffer stride
      const mappedU32 = new Uint32Array(mappedData.buffer);
      const pixelU32 = new Uint32Array(pixelData.buffer);

      // Copy rows accounting for alignment
      for (let row = 0; row < height; row++) {
        const sourceRowStart = (row * bytesPerRow) / 4; // Divide by 4 since we're using 32-bit values
        const targetRowStart = row * width;

        for (let x = 0; x < width; x++) {
          const pixel = mappedU32[sourceRowStart + x];
          // Extract BGRA channels
          const b = (pixel & 0x000000FF);
          const g = (pixel & 0x0000FF00);
          const r = (pixel & 0x00FF0000);
          const a = (pixel & 0xFF000000);

          // Reassemble as RGBA
          pixelU32[targetRowStart + x] = (a) | (b << 16) | (g) | (r >> 16);
        }
      }

      // Create canvas and draw the pixel data
      const img = document.createElement('img');
      img.style.position = 'absolute';

      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = width;
      tempCanvas.height = height;
      const ctx = tempCanvas.getContext('2d')!;
      const imageData = ctx.createImageData(width, height);
      imageData.data.set(pixelData);
      ctx.putImageData(imageData, 0, 0);

      // Convert to data URL and set as image source
      const dataUrl = tempCanvas.toDataURL();
      await new Promise<void>((resolve) => {
        img.onload = () => resolve();
        img.src = dataUrl;
      });

      // Position the overlay absolutely within the parent container
      img.style.position = 'absolute';
      img.style.left = '0';
      img.style.top = '0';
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.objectFit = 'cover';
      img.style.opacity = '100%';

      // Add to parent container
      const parentContainer = canvas.parentElement;
      if (!parentContainer) {
        console.warn('[canvasSnapshot] Canvas has no parent element');
          return;
        }
        parentContainer.appendChild(img);
        entry.overlay = img;

      // Cleanup resources safely
      try {
        if (readbackBuffer) {
          readbackBuffer.unmap();
          readbackBuffer.destroy();
        }
        if (texture) texture.destroy();
        if (depthTexture) depthTexture.destroy();
      } catch (err) {
        console.warn('[canvasSnapshot] Error during resource cleanup:', err);
        // Continue despite cleanup errors - the overlay was already created
      }

      console.log("[canvasSnapshot] Overlay created successfully");
    })
  );
}

/**
 * Removes all canvas overlays created for PDF export
 * Called after PDF generation is complete to restore interactive WebGPU canvases
 */
export function removeCanvasOverlays(): void {
  Object.values(activeCanvases).forEach(entry => {
    if (entry.overlay) {
      entry.overlay.remove();
      delete entry.overlay;
    }
  });
}

genstudio.beforePDF = createCanvasOverlays;
genstudio.afterPDF = removeCanvasOverlays;
