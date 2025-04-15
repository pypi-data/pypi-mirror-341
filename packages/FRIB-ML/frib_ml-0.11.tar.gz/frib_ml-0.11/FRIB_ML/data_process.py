#This module is used for processing training data for training the machine learning model
import h5py
import skimage.transform
import numpy as np

class process:

#Function that takes h5 file and returns a processed numpy array
@classmethod
def h5_process(cls,file_name):
	with h5py.File(file_name, 'r') as f:
		dataset = list(f.keys())[0]
		a = np.array(f[dataset])
		#Process array
		array = skimage.transform.downscale_local_mean(a,(5,5))
		f.close()
		
	return array
