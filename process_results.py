import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from skimage import color
from skimage.registration import phase_cross_correlation

from utils import *

folder = '/Users/ethantae/Downloads/LabWork /55-43/0'
spectrum_extractor = spectrum_extractor()
spectrum_extractor.load_calibration_coefficients('coefficients.csv')
width, height = 500, 500
x, y = 1400, 1700

x_values = np.empty(1)
y_values = np.zeros(1)
max_intensity = np.zeros(1)

#store reference image as starting point (origin)
ref_image = cv2.imread(folder + '/0_0_0_View Sample.bmp')
cropped1 = ref_image[y:y + height, x:x + width]
# cv2.imshow("cropped", cropped1)
# cv2.waitKey(0)

for i in range(8):
    for j in range(8):
        filename = str(i) + '_' + str(j) + '_0_Spectrum_1.bmp'
        # print('processing ' + filename)

        # get spectrum
        wavenumber, intensity, I_sum_horizontal_normalized = spectrum_extractor.extract_spectrum(folder + '/' + filename, use_fixed_ROI=True)
        # save spectrum
        # np.savetxt('results/' + filename + "_spectrum.csv", np.array([wavenumber,intensity]), delimiter=",")
        # print(intensity)
        max_intensity = np.append(max_intensity, np.max(intensity))
        # extrapolate stage position
        view_sample_path = str(i) + '_' + str(j) + '_0_View Sample.bmp'
        raw_image = cv2.imread(folder + '/' + view_sample_path)
        cropped2 = raw_image[y:y + height, x:x + width]
        shift, error, diffphase = phase_cross_correlation(cropped1, cropped2, upsample_factor=10)
        x_values = np.append(x_values, shift[1])
        y_values = np.append(y_values, shift[0])

print(x_values)
print(y_values)
print(max_intensity)

image_1 = plt.imread(folder + '/0_0_0_View Sample.bmp')

#find coordinates of origin in reference image
value, thresh = cv2.threshold(image_1, 250, 255, 0)
M = cv2.moments(thresh)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])

#Use phase correlations and add to origin to develop accurate coordinate grid
x_values = x_values+cX
y_values = y_values+cY


imageplot = plt.imshow(image_1, cmap='gray')
plt.scatter(x_values, y_values, c = max_intensity, cmap = 'plasma', alpha = 0.5, s = 70)
plt.show()

