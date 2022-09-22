# Single Capture and Recaptured Image Classificator

GUI with a CNN-trained image classifier to recognize recaptured images from single captures images. Made for the Master's Thesis "Implementation and Optimization of a Deep Learning-Based Detection Method for Recaptured Images" at [Berlin Hochschule für Technik](https://www.bht-berlin.de/). 

# The Classifier

This classifier is inspired by the work of [[1]](#1), which is a VGGNet[[2]](#2)-inspired convolutional neural network. It takes 64 by 64px subblocks of a larger image and classifies each one individually. After that, blocks with a low contrast are discarded and the remaining ones are used for the final classification.

This CNN was trained with the ICL Dataset[[3]](#3), composed by high-quality images recaptured from an LCD screen with a DSLR camera. In total, there are 900 single capture images taken from 9 different DSLR cameras and 1440 recaptured images from 8 different DSLR cameras.

# The GUI

The GUI consists on a simple window implemented with PyQt5 to input images and obtain the classification of the image as a whole (single capture/recaptured), to see which blocks were used for detection and which ones were incorrectly detected. It is designed to be used with the images of the ICL dataset or similar sized images. 

# References
<a id="1">[1]</a>
Hak-Yeol Choi, Han-Ul Jang, Jeongho Son, Dongkyu Kim, and Heung-Kyu Lee. Content recapture detection based on convolutional neural networks. In Kuinam Kim and Nikolai
Joukov, editors, Information Science and Applications 2017, pages 339–346, Singapore, 2017. Springer Singapore.

<a id="2">[2]</a>
Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for largescale image recognition, 2015

<a id="3">[3]</a>
Hani Muammar and Pier Luigi Dragotti. An investigation into aliasing in images recaptured from an lcd monitor using a digital camera. In 2013 IEEE International Conference on Acoustics, Speech and Signal Processing, pages 2242–2246. IEEE, 2013.
