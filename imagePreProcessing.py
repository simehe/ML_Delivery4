import skimage
import os
from skimage import io
import random
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
TRAININGSET = 0.8


def digitalImagePrep(image, image_name, mode):
    # Feature scaling
    # print (image)

    image = image / float(255)

    # Adding contrast to the image
    image = increaseContrast(image)

    # Augment the picture, dependent on mode
    if (mode == 0):
        image = smoothen(image)
    elif(mode == 1):
        image = sharpen(image)


    print ("")
    print (image_name, shareOfWhitePixels(image, image_name), shareOfWhiteFramePixels(image, image_name))
    print(shareOfWhitePixels(image, image_name) > INVERSION_THRESHOLD_CONTENT)

    # Invert image if necessary
    if shareOfWhiteFramePixels(image, image_name) > INVERSION_THRESHOLD_FRAME or shareOfWhitePixels(image,
                                                                                                    image_name) > INVERSION_THRESHOLD_CONTENT:
        image = invert(image)

    return image


def invert(image):
    return skimage.util.invert(image)


def increaseContrast(image):
    return skimage.exposure.adjust_sigmoid(image, cutoff=0.5, gain=40, inv=False)


def smoothen(image):
    return skimage.restoration.denoise_tv_chambolle(image, weight=0.1, multichannel=True)


def sharpen(image):
    return skimage.util.random_noise(image, mode='gaussian', seed=None, clip=True)


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

    for c in chars:
        reader.readImage(c + "/")
        images = reader.imageHolder
        saveDestination = "mlImageHolder/" + c
        saveDestination2 = "mlImageHolder/" + c + "/" + "test"
        try:
            os.makedirs(saveDestination)
        except OSError as exception:
            print "\nBE CAREFUL! Directory %s already exists." % saveDestination
        try:
            os.makedirs(saveDestination2)
        except OSError as exception:
            print "\nBE CAREFUL! Directory %s already exists." % saveDestination2
        counter = 0
        numberOfTrainingImages = int(len(images) * TRAININGSET)
        for i in range(numberOfTrainingImages):  # Here, I want modify and save each image
            fname1 = c + "_" + str(counter) + ".jpg"
            counter += 1
            fname2  = c + "_" + str(counter) + ".jpg"
            counter += 1
            fname3 = c + "_" + str(counter) + ".jpg"
            counter += 1
            prepped = digitalImagePrep(images[i], fname1, 0)  # Image preprocessing
            prepped2 = digitalImagePrep(images[i], fname2, 1)
            prepped3 = digitalImagePrep(images[i], fname3, 2)
            saveDestination1 = "mlImageHolder/" + c + "/" + fname1
            saveDestination2 = "mlImageHolder/" + c + "/" + fname2
            saveDestination3 = "mlImageHolder/" + c + "/" + fname3
            io.imsave(saveDestination1, prepped)
            io.imsave(saveDestination2, prepped2)
            io.imsave(saveDestination3, prepped3)
        for i in range(numberOfTrainingImages, len(images)):
            fname = c + "_" + str(counter) + ".jpg"
            counter += 1
            prepped = digitalImagePrep(images[i], fname, 2)
            saveDestination = "mlImageHolder/" + c + "/" + "test" + "/" + fname
            io.imsave(saveDestination, prepped)
        reader.clearVector()


main()