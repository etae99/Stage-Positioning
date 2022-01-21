import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

class spectrum_extractor:

	def __init__(self, lambda_ex_nm=785, roi = [556,562]):
		self.lambda_ex_cm = lambda_ex_nm*1e-9/(1e-2)
		self.roi = roi
		self.p = None

	def load_calibration_coefficients(self,filename):
		self.p = np.loadtxt(filename,delimiter = ',')
		print(self.p)

	def extract_spectrum(self,filename, use_fixed_ROI = False, relative_threshold = 0.2):

		# read the image
		I = cv2.imread(filename)
		I = I.astype('float')
		I = I[:,:,0]

		# project along x (wavelength) and identify the location of the spectrum
		I_sum_horizontal = np.sum(I,axis=1)
		I_sum_horizontal_normalized = (I_sum_horizontal-min(I_sum_horizontal))/(max(I_sum_horizontal)-min(I_sum_horizontal))
		
		# crop the image
		if use_fixed_ROI == False:
			idx = I_sum_horizontal_normalized > relative_threshold
			I_cropped = I[idx,:]
			print('width: ' + str(sum(idx)) + ' pixels')
		else:
			I_cropped = I[self.roi[0]:self.roi[1],:]

		# extract the spectrum
		spectrum = np.sum(I_cropped,axis=0)

		# get the wavenumber
		x = range(1920)
		x = np.flip(x)
		lambda_nm = x*self.p[0] + self.p[1]
		lambda_cm = lambda_nm*1e-9/1e-2
		wavenumber_invcm = 1/self.lambda_ex_cm - 1/lambda_cm

		return wavenumber_invcm, spectrum, I_sum_horizontal_normalized

	# def stage_position(self, image1, image2, filepath):
	# 	width, height = 1800, 1800
	# 	x, y = 550, 1100
	#
	# 	ref_image = cv2.imread(filepath + '/0_0_0_Spectrum_0.bmp')
	# 	cropped1 = ref_image[y:y + height, x:x + width]
	#
	# 	for i in range
	# 	raw_image = cv2.imread(filepath +)
