import numpy as np
import cupy as cp
import blur

# Create a simple test pattern
test_image = cp.ones((10, 20, 30), dtype=cp.float32)
# Add a gradient along one dimension to make differences more visible
for i in range(test_image.shape[0]):
    test_image[i, :, :] *= (i + 1)

# Run both implementations
result_original = cp.empty_like(test_image)
result_optimized = cp.empty_like(test_image)

delta = 2  # Small delta for easy debugging
axis = 0  # Test along x-axis

blur.box_1d(test_image, delta, axis=axis, output=result_original)
blur.box_integral(test_image, delta, axis=axis, output=result_optimized)

# Compare results
diff = cp.abs(result_original - result_optimized)
max_diff = cp.max(diff).get()
mean_diff = cp.mean(diff).get()
print(f"Max difference: {max_diff}")
print(f"Mean difference: {mean_diff}")

# Check specific locations where differences occur
if max_diff > 1e-5:
    high_diff_indices = cp.where(diff > max_diff * 0.5)
    print("Sample differences at high-difference locations:")
    for i in range(min(5, len(high_diff_indices[0]))):
        x, y, z = high_diff_indices[0][i], high_diff_indices[1][i], high_diff_indices[2][i]
        print(f"Position ({x},{y},{z}):")
        print(f"  Original: {result_original[x,y,z].get()}")
        print(f"  Optimized: {result_optimized[x,y,z].get()}")
        
        # Print window used by original implementation
        if axis == 0:
            start = max(0, x - delta)
            end = min(test_image.shape[0] - 1, x + delta)
            window = test_image[start:end+1, y, z].get()
        elif axis == 1:
            start = max(0, y - delta)
            end = min(test_image.shape[1] - 1, y + delta)
            window = test_image[x, start:end+1, z].get()
        else:  # axis == 2
            start = max(0, z - delta)
            end = min(test_image.shape[2] - 1, z + delta)
            window = test_image[x, y, start:end+1].get()
            
        print(f"  Window: {window}")
        print(f"  Window mean: {window.mean()}")
