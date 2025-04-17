import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Change "1" to the desired GPU ID

import time
import gc
import cupy as cp
import numpy as np
from ioMicro import read_im, get_local_max_tile
from time import sleep
import cv2
from multiprocessing import Pool, TimeoutError
import time,sys

from tqdm import tqdm

from worker import get_files
from maxima import Maxima

def count_shared_points(array1, array2, tolerance=1e-5):
	shared_count = 0
	# Iterate through each point in array1
	for point1 in array1:
		# Calculate the distances from point1 to all points in array2
		distances = np.linalg.norm(array2 - point1, axis=1)
		# Check if the minimum distance is below the tolerance
		if np.any(distances < tolerance):
			shared_count += 1
	return shared_count

def norm_slices(image, ksize=50):
	xp = cp.get_array_module(image)
	if xp == np:
		from scipy.ndimage import convolve
	else:
		from cupyx.scipy.ndimage import convolve

	image = image.astype(xp.float32)  # Ensure correct type
	kernel = xp.ones((ksize, ksize), dtype=xp.float32) / (ksize * ksize)

	padded = np.pad(image, ((1,0) ,(1, 0), (1, 0)), mode='reflect')
	# Apply blur to each slice in parallel without looping in Python
	blurred = convolve(padded, kernel[None, :, :], mode="nearest")

	return image - blurred[0:image.shape[0], 0:image.shape[1], 0:image.shape[2]]



if __name__ == "__main__":
	psf_file = '../psfs/dic_psf_60X_cy5_Scope5.pkl'
	psfs = np.load(psf_file, allow_pickle=True)
	fov = 'Conv_zscan1_002.zarr'
	fld = '/data/07_22_2024__PFF_PTBP1/H0_AER_set1'
	icol = 0
	im_ = read_im(fld+os.sep+fov)
	#im__ = np.array(im_[icol],dtype=np.float32)
	im__ = np.array(im_[0])
	### new method
	fl_med = '../flat_field/Scope5_med_col_raw'+str(icol)+'.npz'
	if os.path.exists(fl_med):
		im_med = np.array(np.load(fl_med)['im'],dtype=np.float32)
		im_med = cv2.blur(im_med,(20,20))
		im__ = im__/im_med*np.median(im_med)
		im__ = im__.astype(np.float16)
	else:
		print(fl_med)
		print("Did not find flat field")


	maxima = Maxima()

	cim = cp.asarray(im__)
	cnim = norm_slices(cim)
	nim = cp.asnumpy(cnim)
	start = time.time()
	local0 = maxima.get_local(cnim , im_raw=cim)
	local0 = cp.asnumpy(local0)
	print(local0.shape)
	print(local0)

	from ioMicro import get_local_maxfast
	local1 = get_local_maxfast(nim , 2500,  im_raw=im__)
	print()
	print(local1.shape)
	print(local1)

	shared = count_shared_points(local0[:,:3], local1[:,:3], tolerance=1)
	print(shared)






