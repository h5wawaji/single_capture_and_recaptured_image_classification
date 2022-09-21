#import packages
import cv2
import tensorflow
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from PIL.Image import Image
import skimage
from skimage.feature.texture import greycomatrix, greycoprops
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array, load_img
from numpy import loadtxt
from keras.models import load_model


class Classification():
    """
    Class using the trained neural network to classify images as recaptured or single capture.
    """
    def __init__(self, image):
        self.batch_size = 256
        self.channels = 3
        self.image = str(image)
        self.image_height = 1344
        self.image_width = 2048
        self.block_size = 64
        self.model = None
        self.prediction_vector = []
        self.used_blocks_vector = []
        self.result = 0

    def load_model(self):
        """
        Loads the already trained neural model and its weights.
        """
        self.model = load_model("model.h5")
        self.model.load_weights("weights_model.h5")

    def pre_processing(self):
        """
        Pre-processing function. Takes the original image and divides it into sub-blocks.
        Then, takes a measure of the contrast in the sub-blocks, if its over a threshold, the sub-
        block is added to a vector, if not it is discarded.
        :return: A vector of the sub-blocks over certain contrast threshold.
        """
        X = []
        contrast_vec = []

        original_image = cv2.imread(self.image, cv2.IMREAD_COLOR)
        image_height, image_width, image_channels = original_image.shape
        if image_height <= self.image_height:
            self.image_height = round(image_height/64) *64
            self.image_width = round(image_width/64) * 64
        else:
            pass

        image_to_slice = cv2.resize(cv2.imread(self.image, cv2.IMREAD_COLOR), (self.image_width, self.image_height),
                                    interpolation=cv2.INTER_CUBIC)
        image_to_slice = cv2.cvtColor(image_to_slice, cv2.COLOR_BGR2RGB)
        # now we create the blocks
        sub_blocks_list = [image_to_slice[x:x + self.block_size, y:y + self.block_size]
                           for x in range(0, self.image_height, self.block_size)
                           for y in range(0, self.image_width, self.block_size)]
        for sub_block in sub_blocks_list:
            gray_image = cv2.cvtColor(sub_block, cv2.COLOR_BGR2GRAY)
            co_ocurrence = greycomatrix(gray_image, [1], [0, np.pi/2], normed=True)
            contrast = greycoprops(co_ocurrence, 'contrast')
            contrast_vec.append(sum(sum(contrast)))
            if sum(sum(contrast))/2 > 20.0:
                X.append(sub_block)
                self.used_blocks_vector.append(1)
            else:
                self.used_blocks_vector.append(0)
                pass
        return X

    def classify(self, X):
        """
        Function that classifies the sub-blocks into single capture (0) or recaptured (1) images
        using the trained neural network.
        :param X: Vector with sub-blocks of an image. These sub-blocks are over certain contrast threshold
        """
        i, n_used = 0, 0
        acc = []
        x = np.array(X) / 255.0  # normalization between 0 and 1
        try:
            pred = self.model(x, training=False)
            pred = np.array(np.round(pred))
            i += 1
            if pred.mean() > 0.5:
                acc.append(1)
            else:
                acc.append(0)
        except:
            n_used += 1
            pass

        self.prediction_vector = np.array(pred)

    def prediction(self):
        """
        Function made to load the model and predict the sub-blocks from an image.
        :return: The classification of the whole image.
        """
        self.load_model()
        x = self.pre_processing()
        self.classify(x)
        self.result = np.round(self.prediction_vector.mean())

        return np.round(self.prediction_vector.mean())

    def info(self):
        """
        Function to get the classification of each sub-block.
        :return: A vector with the classification of each sub-block.
        """
        return self.prediction_vector

    def create_mask(self):
        """
        Function to create the mask for correctly classified sub-blocks.
        :return: A new image with the mask applied.
        """
        if self.result == 1:
            image = self.create_mask_recaptured()  #for images classified as recaptured
        else:
            image = self.create_mask_single_capture()  #for images classified as single capture

        return image

    def create_mask_recaptured(self):
        """
        Function that changes the color of a sub-blocks depending on the classification of it.
        The sub-block is filled with black if it was not used for the classification, it is red-tinted if it
        is incorrectly classified and stays the same if it is correctly classified.
        :return: A new image with sub-blocks of different colors.
        """
        j, k, l, m = 0, 0, 0, 0
        color_image = np.full((self.block_size,self.block_size,3), (0,0,255), np.uint8)
        image = cv2.resize(cv2.imread(self.image, cv2.IMREAD_COLOR), (self.image_width, self.image_height),
                           interpolation=cv2.INTER_CUBIC)
        for k in range(0, self.image_height, 64):
            for l in range(0, self.image_width, 64):
                if self.used_blocks_vector[j] == 1:
                    if self.prediction_vector[m] < 0.5:
                        image[k:k + 64, l:l + 64,:] = cv2.add(image[k:k + 64, l:l + 64,:],color_image)
                    j += 1
                    l += 1
                    m += 1
                else:
                    image[k:k + 64, l:l + 64] = 0
                    j += 1
                    l += 1
            k += 1
        return image

    def create_mask_single_capture(self):
        """
        Function that changes the color of a sub-blocks depending on the classification of it.
        The sub-block is filled with black if it was not used for the classification, it is red-tinted if it
        is incorrectly classified and stays the same if it is correctly classified.
        :return: A new image with sub-blocks of different colors.
        """
        j, k, l, m = 0, 0, 0, 0
        color_image = np.full((self.block_size,self.block_size,3), (0,0,255), np.uint8)
        image = cv2.resize(cv2.imread(self.image, cv2.IMREAD_COLOR), (self.image_width, self.image_height),
                           interpolation=cv2.INTER_CUBIC)
        for k in range(0, self.image_height, 64):
            for l in range(0, self.image_width, 64):
                if self.used_blocks_vector[j] == 1:
                    if self.prediction_vector[m] > 0.5:
                        image[k:k + 64, l:l + 64,:] = cv2.add(image[k:k + 64, l:l + 64,:],color_image)
                    j += 1
                    l += 1
                    m += 1
                else:
                    image[k:k + 64, l:l + 64] = 0
                    j += 1
                    l += 1
            k += 1
        return image




