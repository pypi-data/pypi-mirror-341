import cupy as cp

# Define CUDA kernel for local maxima detection
local_maxima_kernel = cp.RawKernel(r'''
extern "C" __global__
void find_local_maxima(const float* image, const int* coords, const bool* above_threshold,
					   bool* is_local_max, int num_points, int delta,
					   int depth, int height, int width) {
	int idx = blockDim.x * blockIdx.x + threadIdx.x;
	if (idx >= num_points || !above_threshold[idx]) {
		return;
	}
	
	int z = coords[idx * 3];
	int x = coords[idx * 3 + 1];
	int y = coords[idx * 3 + 2];
	if (z < 0 || z >= depth || x < 0 || x >= height || y < 0 || y >= width) {
		return;
	}
	
	float center_value = image[z * height * width + x * width + y];
	bool is_max = true;

	// Check all neighbors in the spherical mask
	for (int dz = -delta; dz <= delta; dz++) {
		for (int dx = -delta; dx <= delta; dx++) {
			for (int dy = -delta; dy <= delta; dy++) {
				// Skip the center point
				if (dz == 0 && dx == 0 && dy == 0) {
					continue;
				}
				
				// Check if spherical
				if ((dz*dz + dx*dx + dy*dy) > (delta*delta)) {
					continue;
				}
				
				int nz = z + dz;
				int nx = x + dx;
				int ny = y + dy;
				
				// Boundary check
				if (nz >= 0 && nz < depth && nx >= 0 && nx < height && ny >= 0 && ny < width) {
					float neighbor_value = image[nz * height * width + nx * width + ny];
					if (center_value < neighbor_value) {
						is_max = false;
						break;
					}
				}
			}
			if (!is_max) break;
		}
		if (!is_max) break;
	}
	
	is_local_max[idx] = is_max;
}
''', 'find_local_maxima')

def find_local_maxima(image, threshold):
	# Ensure the image is in C-contiguous order for the kernel
	if not image.flags.c_contiguous:
		image = cp.ascontiguousarray(image)
	
	# Find points above threshold
	above_threshold = image > threshold
	above_threshold_flat = above_threshold.ravel()
	
	# Get coordinates of all points
	coords = cp.stack(cp.indices(image.shape), axis=0).reshape(3, -1).T.astype(cp.int32)
	
	# Allocate output array
	is_local_max = cp.zeros(image.size, dtype=cp.bool_)
	
	# Set up kernel parameters
	threads_per_block = 256
	blocks_per_grid = (image.size + threads_per_block - 1) // threads_per_block
	
	# Call the kernel
	delta = 1  # Radius of spherical mask
	local_maxima_kernel((blocks_per_grid,), (threads_per_block,), 
					   (image.ravel(), coords, above_threshold_flat, 
						is_local_max, image.size, delta,
						image.shape[0], image.shape[1], image.shape[2]))

	# Get coordinates of local maxima
	local_max_indices = cp.where(is_local_max)[0]
	if len(local_max_indices) > 0:
		local_max_coords = coords[local_max_indices]
		z = local_max_coords[:, 0]
		x = local_max_coords[:, 1]
		y = local_max_coords[:, 2]
		return z, x, y
	else:
		return cp.array([], dtype=cp.int32), cp.array([], dtype=cp.int32), cp.array([], dtype=cp.int32)

