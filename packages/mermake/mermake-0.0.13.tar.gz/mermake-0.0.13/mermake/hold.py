import cupy as cp
from math import prod

# Optimized Kernel for MaxFast, including both detection and delta fitting
local_maxima_kernel = cp.RawKernel(r'''
extern "C" __global__
void local_maxima(const float* image, float threshold,
								int delta, int delta_fit,
								float* z_out, float* x_out, float* y_out, unsigned int* count,
								int depth, int height, int width, int max_points) {
	// Get flattened index
	int idx = blockDim.x * blockIdx.x + threadIdx.x;
	if (idx >= depth * height * width) {
		return;
	}

	// Convert flat index to 3D coordinates
	int z = idx / (height * width);
	int temp = idx % (height * width);
	int x = temp / width;
	int y = temp % width;

	float center_value = image[idx];

	// Check if above threshold
	if (center_value <= threshold) {
		return;
	}

	// Check if it's a local maximum in the neighborhood
	bool is_max = true;
	for (int dz = -delta; dz <= delta; dz++) {
		for (int dx = -delta; dx <= delta; dx++) {
			for (int dy = -delta; dy <= delta; dy++) {
				// Skip the center point
				if (dz == 0 && dx == 0 && dy == 0) {
					continue;
				}

				// Check if within spherical mask
				if ((dz*dz + dx*dx + dy*dy) > (delta*delta)) {
					continue;
				}

				int nz = z + dz;
				int nx = x + dx;
				int ny = y + dy;
				

				// Apply reflect only if out of bounds
				if (nz < 0 || nz >= depth) {
					nz = (nz < 0) ? -nz : 2 * depth - nz - 2;
				}
				if (nx < 0 || nx >= height) {
					nx = (nx < 0) ? -nx : 2 * height - nx - 2;
				}
				if (ny < 0 || ny >= width) {
					ny = (ny < 0) ? -ny : 2 * width - ny - 2;
				}

				if (center_value < image[nz * height * width + nx * width + ny]) {
					is_max = false;
					break;
				}
			}
			if (!is_max) break;
		}
		if (!is_max) break;
	}

	// If it's a local maximum, refine the location with delta fitting
	if (is_max) {
		/*
		// Define fitting region around the maxima
		int z_min = max(0, z - delta_fit), z_max = min(depth, z + delta_fit + 1);
		int x_min = max(0, x - delta_fit), x_max = min(height, x + delta_fit + 1);
		int y_min = max(0, y - delta_fit), y_max = min(width, y + delta_fit + 1);

		// Search for the maximum in the neighborhood to refine the position
		float max_val = center_value;
		float refined_z = z, refined_x = x, refined_y = y;

		for (int dz = z_min; dz < z_max; dz++) {
			for (int dx = x_min; dx < x_max; dx++) {
				for (int dy = y_min; dy < y_max; dy++) {
					float value = image[dz * height * width + dx * width + dy];
					if (value > max_val) {
						max_val = value;
						refined_z = dz;
						refined_x = dx;
						refined_y = dy;
					}
				}
			}
		}

		// Store the refined coordinates if within bounds
		unsigned int pos = atomicAdd(count, 1);
		if (pos < max_points) {
			z_out[pos] = refined_z;
			x_out[pos] = refined_x;
			y_out[pos] = refined_y;
		}
		*/
		// If it's a local maximum, add to output
		if (is_max) {
			unsigned int pos = atomicAdd(count, 1);
			if (pos < max_points) {
            z_out[pos] = z;
            x_out[pos] = x;
            y_out[pos] = y;
			}
		}
	}
}
''', 'local_maxima')

def find_local_maxima(image, threshold, delta, delta_fit):
	"""
	Find and refine local maxima in a 3D image directly on GPU, including delta fitting.
	
	Args:
		image: 3D CuPy array
		threshold: Minimum value for local maxima detection
		delta_fit: Size of the fitting neighborhood
	
	Returns:
		Tuple of (z, x, y) coordinates for refined local maxima
	"""
	# Ensure the image is in C-contiguous order for the kernel
	if not image.flags.c_contiguous:
		image = cp.ascontiguousarray(image)

	max_points = prod(image.shape) + 1

	# Allocate output arrays
	out = cp.zeros([max_points, 3], dtype=cp.float32)
	count = cp.zeros(1, dtype=cp.uint32)

	# Set up kernel parameters
	threads_per_block = 256
	blocks_per_grid = (image.size + threads_per_block - 1) // threads_per_block

	# Call the kernel
	local_maxima_kernel((blocks_per_grid,), (threads_per_block,), 
					(image.ravel(), threshold, delta, delta_fit,
					 out[:, 0], out[:, 1], out[:, 2], count,
					 image.shape[0], image.shape[1], image.shape[2], max_points))

	# Return only the valid parts of the output arrays
	mask = out.all(axis=1)
	return out[mask]

if __name__ == "__main__":
	import numpy as np
	import torch
	from ioMicro import get_local_maxfast_tensor
	# Example Usage
	A = cp.random.rand(10, 3000, 3000)
	B = cp.asnumpy(A)
	local = find_local_maxima(A, 0.9, 1, 3)
	print(local.shape)
	print(local)
	tem = get_local_maxfast_tensor(B,th_fit=0.9,im_raw=None,dic_psf=True,delta=1,delta_fit=0,sigmaZ=1,sigmaXY=1.5,gpu=False)
	print(tem.shape)
	print(tem)
