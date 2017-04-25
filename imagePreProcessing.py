import skimage
import os
from skimage import io
from skimage import filters
from PIL import Image
import numpy as np
import string
from imageReading import ImageReader
from scipy import ndimage as ndi
from skimage import feature
from skimage.restoration import (denoise_tv_chambolle, denoise_bilateral,
                                 denoise_wavelet, estimate_sigma)
from skimage.filters import roberts, sobel, scharr, prewitt

INVERSION_THRESHOLD_FRAME = 0.5  # If the share of white pixels in the image frame is larger than this, we invert the image
INVERSION_THRESHOLD_CONTENT = 0.55  # If the share of white pixels in the image is larger than this, we invert the image
FAIR_AMOUNT_OF_WHITE_PIXELS = 0.5  # If the share of white pixels in the image is larger than this, we consider the letter too close-up and we add a
THRESHOLD_CONSIDERED_WHITE = 0.6  # Pixels with value greater than this value are considered white
THRESHOLD_CONSIDERED_SHARP = 0.8
THRESHOLD_CONSIDERED_BLURRY = 0.2

def digitalImagePrep(image, image_name):
	# Feature scaling
	#print (image)
	for i in range(len(image)):
		for j in range(len(image[i])):
			image[i][j] = float(image[i][j])
    
	image = image / 255
    
	# Adding contrast to the image
	image = increaseContrast(image)


	# Compute the Canny filter for two values of sigma
	edges1 = sobel(image)
	edges2 = feature.canny(image, sigma=3)

	# Computing the magnitude of the sharpest edge
	sharpestEdge = 0.0
	for i in edges1:
		for j in i:
			if(sharpestEdge<j):
				sharpestEdge = j
	
	print ("Sharpest edge", sharpestEdge)
	#sharpestEdge = max(edges1)
	#sharpestEdge2 = max(edges2)


	if sharpestEdge > THRESHOLD_CONSIDERED_SHARP:
		image = smoothen(image)

	if sharpestEdge < THRESHOLD_CONSIDERED_BLURRY:
		image = sharpen(image)

	print ("")
	print (image_name, shareOfWhitePixels(image, image_name), shareOfWhiteFramePixels(image, image_name))
	print(shareOfWhitePixels(image, image_name) > INVERSION_THRESHOLD_CONTENT)

	# Invert image if necessary
	if shareOfWhiteFramePixels(image, image_name) > INVERSION_THRESHOLD_FRAME or shareOfWhitePixels(image, image_name) > INVERSION_THRESHOLD_CONTENT:
		image = invert(image)

	return image


def invert(image):
    return skimage.util.invert(image)


def increaseContrast(image):
    return skimage.exposure.adjust_sigmoid(image, cutoff=0.5, gain=10, inv=False)


def smoothen(image):
    return denoise_tv_chambolle(image, weight=0.1, multichannel=True)


def sharpen(image):
    return skimage.util.random_noise(image, mode='gaussian', seed=None, clip=True, **kwargs)


def shareOfWhiteFramePixels(image, image_name):
    (w, h) = get_image_size(image_name)

    circumference = 2 * (h + w)

    whiteCount = 0.0
    for i in range(h):
        whiteCount += 1 if image[i][0] > THRESHOLD_CONSIDERED_WHITE else 0
        whiteCount += 1 if image[i][w - 1] > THRESHOLD_CONSIDERED_WHITE else 0

    for j in range(w):
        whiteCount += 1 if image[0][j] > THRESHOLD_CONSIDERED_WHITE else 0
        whiteCount += 1 if image[h - 1][j] > THRESHOLD_CONSIDERED_WHITE else 0

    return whiteCount / circumference


def shareOfWhitePixels(image, image_name):
    (w, h) = get_image_size(image_name)
    whiteCount = 0.0

    for i in range(h):
        for j in range(w):
            whiteCount += 1 if image[i][j] > THRESHOLD_CONSIDERED_WHITE else 0

    return whiteCount / (h * w)


def get_image_size(fname):

    return 20, 20


def tester():
    chars = string.lowercase[:]
    nums = range(9)
    print("name \t whiteContent \t whiteFrame")
    for c in chars:
        i = 0
        try:
            fname = "chars74k-lite-preprocessed/" + c + "_" + str(i)
            print (fname)
            image = io.imread(fname + ".jpg")

            prepped = digitalImagePrep(image, fname + ".jpg")
            w, h = get_image_size(fname + ".jpg")
            io.imsave(fname + ".jpg", prepped)
        except:
            print("Error")


def main():
    #
    chars = string.ascii_lowercase[:]  # List of chars a-z
    reader = ImageReader("chars74k-lite/")

    for c in chars[:]:
        reader.readImage(c + "/")
        images = reader.imageHolder
        saveDestination = "mlImageHolder/" + c
        try:
            os.makedirs(saveDestination)
        except OSError as exception:
            print ("\nBE CAREFUL! Directory %s already exists." % saveDestination)
        for i in range(len(images)):  # Here, I want modify and save each image
            fname = c + "_" + str(i) + ".jpg"
            prepped = digitalImagePrep(images[i], fname)  # Image preprocessing
            saveDestination = "mlImageHolder/" + c + "/" + fname
            io.imsave(saveDestination, prepped)

        reader.clearVector()


main()