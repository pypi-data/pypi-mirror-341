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

import napari
from tqdm import tqdm

from worker_old import get_files
from maxima import Maxima
from deconvolver import Deconvolver
from utils import norm_image

psf_file = '../psfs/dic_psf_60X_cy5_Scope5.pkl'
master_data_folders = ['/data/07_22_2024__PFF_PTBP1']
save_folder = 'output'
lib_fl = "../codebooks/codebook_code_color2__ExtraAaron_8_6_blank.csv"
iHm = 1 ; iHM = 16
def main_do_compute_fits(save_folder,fld,fov,icol,save_fl,psf,old_method):
	im_ = read_im(fld+os.sep+fov)
	im__ = np.array(im_[icol],dtype=np.float32)
	
	### new method
	fl_med = '../flat_field/Scope5_med_col_raw'+str(icol)+'.npz'
	if os.path.exists(fl_med):
		im_med = np.array(np.load(fl_med)['im'],dtype=np.float32)
		im_med = cv2.blur(im_med,(20,20))
		im__ = im__/im_med*np.median(im_med)
	else:
		print("Did not find flat field")
	try:
		Xh = get_local_max_tile(im__,th=3600,s_ = 300,pad=100,psf=psf,plt_val=None,snorm=30,gpu=True,
								deconv={'method':'cupy','beta':0.0001},
								delta=1,delta_fit=3,sigmaZ=1,sigmaXY=1.5)
	except:
		Xh = get_local_max_tile(im__,th=3600,s_ = 300,pad=100,psf=psf,plt_val=None,snorm=30,gpu=False,
								deconv={'method':'wiener','beta':0.0001},
								delta=1,delta_fit=3,sigmaZ=1,sigmaXY=1.5)

	np.savez_compressed(save_fl,Xh=Xh)

def compute_fits(save_folder,fov,all_flds,redo=False,ncols=4,psf_file = psf_file,try_mode=True,old_method=False):
	psf = np.load(psf_file,allow_pickle=True)
	for fld in tqdm(all_flds):
		for icol in range(ncols-1):
			tag = os.path.basename(fld)
			save_fl = save_folder+os.sep+fov.split('.')[0]+'--'+tag+'--col'+str(icol)+'__Xhfits.npz'
			if not os.path.exists(save_fl) or redo:
				if try_mode:
					try:
						main_do_compute_fits(save_folder,fld,fov,icol,save_fl,psf,old_method)
					except:
						print("Failed",fld,fov,icol)
				else:
					main_do_compute_fits(save_folder,fld,fov,icol,save_fl,psf,old_method)			       
def compute_main_f(save_folder,all_flds,fov,set_,ifov,redo_fits,redo_drift,redo_decoding,try_mode,old_method):
	start = time.time()
	psf_file = '../psfs/dic_psf_60X_cy5_Scope5.pkl'
	compute_fits(save_folder,fov,all_flds,psf_file=psf_file, redo=redo_fits,try_mode=try_mode,old_method=old_method)

def main_f(set_ifov,redo_fits = False,redo_drift=False,redo_decoding=False,try_mode=False,old_method=False):
    set_,ifov = set_ifov
    save_folder,all_flds,fov = get_files(set_ifov, iHm=iHm, iHM=iHM)
    if True:
        if try_mode:
            try:
                compute_main_f(save_folder,all_flds,fov,set_,ifov,redo_fits,redo_drift,redo_decoding,try_mode,old_method)
            except:
                print("Failed within the main analysis:")
        else:
            compute_main_f(save_folder,all_flds,fov,set_,ifov,redo_fits,redo_drift,redo_decoding,try_mode,old_method)

        return set_ifov


def image_generator(hybs, fovs):
    """ Generator that yields images from disk one by one """
    for all_flds, fov in zip(hybs, fovs):
        for hyb in all_flds:
            file = os.path.join(hyb, fov)
            yield read_im(file)  # Read and yield image lazily

if __name__ == "__main__":
	psf_file = '../psfs/dic_psf_60X_cy5_Scope5.pkl'
	psfs = np.load(psf_file, allow_pickle=True)
	fov = 'Conv_zscan1_002.zarr'
	fld = '/data/07_22_2024__PFF_PTBP1/H0_AER_set1'
	im = np.array(read_im(fld+os.sep+fov))
	image = np.empty_like(im).astype(np.float32)
	decon = np.empty_like(im).astype(np.float32)
	for icol in range(len(im)):
		fl_med = '../flat_field/Scope5_med_col_raw'+str(icol)+'.npz'
		im_med = np.array(np.load(fl_med)['im'],dtype=np.float32)
		im_med = cv2.blur(im_med,(20,20))
		image[icol] = im[icol] / im_med * np.median(im_med)
		#image = image.astype(np.float32)

	shape = (40,3000,3000)

	'''
	from deconvolver import full_deconv
	viewer = napari.Viewer()
	cim = cp.asarray(image[0])
	key = (0,1500,1500)
	#deconv = full_deconv(cim, psfs={key:psfs[key]})
	#viewer.add_image(cp.asnumpy(deconv), name='single psf')
	deconv = full_deconv(cim, psfs=psfs, beta=0.0001)
	viewer.add_image(cp.asnumpy(deconv), name='multi psf')
	napari.run()
	exit()
	'''

	hyb_deconvolver = Deconvolver(psfs, shape, tile_size=300, overlap=89, zpad=39, beta=0.01)
	dapi_deconvolver = Deconvolver(psfs, shape, tile_size=300, overlap=89, zpad=19, beta=0.01)

	maxima = Maxima(threshold = 3600, xp=np)	
	for icol in range(len(image)-1):
		deconved = hyb_deconvolver.apply(cp.asarray(image[-1]))
		deconved = norm_image(deconved)
		deconved /= deconved.std()
		decon[icol] = cp.asnumpy(deconved)
	icol = -1
	deconved = dapi_deconvolver.apply(cp.asarray(image[icol]))
	deconved = norm_image(deconved)
	deconved /= deconved.std()
	decon[icol] = cp.asnumpy(deconved)

	mempool = cp.get_default_memory_pool()
	for obj in gc.get_objects():
		if isinstance(obj, cp.ndarray):
			print(f"CuPy array with shape {obj.shape} and dtype {obj.dtype}")
			print(f"Memory usage: {obj.nbytes / 1024**2:.2f} MB")  # Convert to MB
	print(f"Used memory after: {mempool.used_bytes() / 1024**2:.2f} MB")

	viewer = napari.Viewer()
	viewer.add_image(im, name='original')
	viewer.add_image(image, name='corrected')
	viewer.add_image(decon, name='deconv')
	coords = maxima.apply(decon[0])[:,:3]
	viewer.add_points(coords, size=7, edge_color='yellow', name="new", face_color='transparent', opacity=0.8,)
	'''
	tnorm0,Xh0 = get_local_max_tile(image[0],th=3600,s_ = 300,pad=100,psf=psfs,plt_val=None,snorm=30,gpu=True,
                                deconv={'method':'wiener','beta':0.0001},
                                delta=1,delta_fit=3,sigmaZ=1,sigmaXY=1.5)
	coords0 = Xh0[:,:3]
	viewer.add_points(coords0, size=7, edge_color='red', name="old", face_color='transparent', opacity=0.8,)
	'''
	napari.run()
	exit()

	#tnorm0,Xh0 = get_local_max_tile(im__, psf=psfs, pad=100)
	#print(Xh0.shape)
	#print(Xh0)
	
	tnorm = np.empty_like(im__)
	cim = cp.asarray(im__)
	Xhf = list()
	for x,y,tile in hyb_deconvolver.tile_wise(cim):
		#tile_norm = norm_image(tile)
		im = cp.asnumpy(tile)
		tnorm[:,x:x+300,y:y+300] = norm_slice(im)[:,89:-89,89:-89]
		tile_norm = cp.asarray(norm_slice(im))
		Xh = maxima.apply(tile_norm, im_raw=tile)
		# use old code for now
		keep = cp.all(Xh[:,1:3] < 300+89, axis=-1)
		keep &= cp.all(Xh[:,1:3] >= 89, axis=-1)
		Xh = Xh[keep]
		Xh[:,1] += x - 89 
		Xh[:,2] += y - 89
		if len(Xh):
			Xhf.append(Xh)
	Xhf = cp.vstack(Xhf)
	Xhf = cp.asnumpy(Xhf)
	print(Xhf.shape)
	print(Xhf)
	#from time_test import count_shared_points 
	#shared = count_shared_points(Xh0[:,:3], Xhf[:,:3], tolerance=3)
	#print(shared, ' shared')

	import numpy as np

	# Example data: two sets of zxy coordinates
	#coords1 = Xh0[:,:3]
	#coords2 = Xhf[:,:3]
	deconv = cp.asnumpy(hyb_deconvolver.apply(cp.asarray(im__)))
	viewer = napari.Viewer()
	viewer.add_image(im__, name='original')
	#viewer.add_image(deconv0, name='torch deconv')
	#viewer.add_image(deconv1, name='cupy deconv')
	#tnorm0 = tnorm0.astype(np.float64)
	tnorm = tnorm.astype(np.float64)
	#viewer.add_image(tnorm0, name='torch normalized')
	viewer.add_image(tnorm, name='cupy normalized')
	#tnorm = tnorm/np.std(tnorm)
	#viewer.add_image(tnorm0, name='torch normalized/')
	#viewer.add_image(tnorm, name='cupy normalized/')
	#viewer.add_points(coords1, size=7, edge_color='red', name="old", face_color='transparent', opacity=0.8,)
	#viewer.add_points(coords2, size=7, edge_color='yellow', name="new", face_color='transparent', opacity=0.8,)

	napari.run()
	exit()






	'''
	items = [(set_,ifov) for set_ in ['_set1'] for ifov in range(1,11)]



	psf_file = '../psfs/dic_psf_60X_cy5_Scope5.pkl'
	im_med = list()
	for icol in [0,1,2,3]:
		fl_med = '../flat_field/Scope5_med_col_raw'+str(icol)+'.npz'
		tem = np.array(np.load(fl_med)['im'],dtype=np.float32)
		med = cv2.blur(tem,(20,20))
		med /= np.median(med)
		im_med.append(med)
	im_med = cp.asarray(np.stack(im_med))
	
	psfs = np.load(psf_file, allow_pickle=True)
	deconvolver = Deconvolver(psfs, 39, tile_size=300)
	hybs = list()
	fovs = list()
	for item in items[:3]:
		save_folder,all_flds,fov = get_files(item, iHm=iHm, iHM=iHM)
		hybs.append(all_flds)
		fovs.append(fov)
	maxima = Maxima()
	start = time.time()
	for im in image_generator(hybs, fovs):
		cim = cp.asarray(im).astype(cp.float32)
		cim /= im_med[:, cp.newaxis, :, :] 
		for icol in [0,1,2]:
			Xhf = list()
			for tile in deconvolver.tile_wise(cim[icol]):
				tile_norm = norm_slices(tile)
				Xh = maxima.get_local(tile_norm, im_raw=tile)
				# use old code for now
				keep = cp.all(Xh[:,1:3] < (300+89/2), axis=-1)
				keep &= cp.all(Xh[:,1:3] >= 89/2, axis=-1)
				Xh = Xh[keep]
				# I guess I need to calculate the positions, do later
				Xh[:,1]+=0
				Xh[:,2]+=0
				if len(Xh):
					Xhf.append(Xh)
			Xhf = cp.vstack(Xhf)

			#np.savez_compressed(f'{base}{fov}',Xh=Xh)
	end = time.time()
	print(f"new class time: {end - start:.6f} seconds")
	'''

	#exit()
	'''
	start = time.time()
	with Pool(processes=4) as pool:
		print('starting pool')
		result = pool.map(main_f, items)
	end = time.time()
	print(f"torch (tiled parallel) time: {end - start:.6f} seconds")
	'''
