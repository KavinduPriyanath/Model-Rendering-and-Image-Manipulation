import cv2
import numpy as np


def convert_to_grayscale(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # convert to grayscale
    # cvtColor -> converts an image from one color space to another
    # ( image, color_space )
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # return grayscale image
    return gray_img


def sharpen_image(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # sharpen image filter
    # [ -1 -1 -1 ]
    # [ -1  9 -1 ]
    # [ -1 -1 -1 ]
    sharpen_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    # apply sharpen filter
    # filter2D -> convolves an image with the kernel
    # ( image, depth, kernel )
    sharpened_img = cv2.filter2D(img, -1, sharpen_filter)

    # return sharpened image
    return sharpened_img


def blur_image_with_mean_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # blur image filter
    # [ 1 1 1 1 ]
    # [ 1 1 1 1 ]
    # [ 1 1 1 1 ] / 16
    blur_filter = np.ones((4, 4), np.float32) / 16

    # apply blur filter
    blurred_img = cv2.filter2D(img, -1, blur_filter)

    # return blurred image
    return blurred_img


def gaussian_smoothing(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # gaussian filter
    gaussian_filtering = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16

    # apply gaussian filter
    gaussian_blurred_img = cv2.filter2D(img, -1, gaussian_filtering)

    # return gaussian blurred image
    return gaussian_blurred_img


def min_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply min filter
    # erode -> erodes an image by using a specific structuring element
    # ( image, kernel, iterations )
    min_filtered_img = cv2.erode(img, np.ones((3, 3), np.uint8), iterations=1)

    # return min filtered image
    return min_filtered_img


def max_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply max filter
    # dilate -> dilates an image by using a specific structuring element
    # ( image, kernel, iterations )
    max_filtered_img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=1)

    # return max filtered image
    return max_filtered_img


def mean_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply mean filter
    # blur -> blurs an image using the normalized box filter
    # ( image, kernel )
    mean_filtered_img = cv2.blur(img, (3, 3))

    # return mean filtered image
    return mean_filtered_img


def median_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply median filter
    # medianBlur -> blurs an image using the median filter
    # ( image, kernel )
    median_filtered_img = cv2.medianBlur(img, 3)

    # return median filtered image
    return median_filtered_img


def midpoint_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply midpoint filter
    # midpoint filtering = (min filtering + max filtering) / 2
    min_filtered_img = min_filtering(img)
    max_filtered_img = max_filtering(img)
    midpoint_filtered_img = (min_filtered_img + max_filtered_img) / 2

    # return midpoint filtered image
    return midpoint_filtered_img


def laplacian_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply laplacian filter
    # Laplacian -> calculates the Laplacian of an image
    # ( image, depth )
    laplacian_filtered_img = cv2.Laplacian(img, cv2.CV_64F)

    # return laplacian filtered image
    return laplacian_filtered_img


def sobel_filtering(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply sobel filter
    # Sobel -> calculates the first, second, third, or mixed image derivatives using an extended Sobel operator
    # ( image, depth, xorder, yorder, ksize )
    sobel_filtered_img = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    # return sobel filtered image
    return sobel_filtered_img


def canny_edge_detection(img):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # apply canny edge detection
    # Canny -> finds edges in an image using the Canny algorithm
    # ( image, threshold1, threshold2 )
    canny_edge_detected_img = cv2.Canny(img, 100, 200)

    # return canny edge detected image
    return canny_edge_detected_img


def threshold_an_image(img, threshold):

    # check if img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # check if threshold is a number
    if type(threshold) != int and type(threshold) != float:
        raise TypeError('threshold must be a number')

    # check whether it is grayscale or not
    if len(img.shape) != 2:
        # convert to grayscale
        img = convert_to_grayscale(img)

    # apply thresholding
    # threshold -> applies a fixed-level threshold to each array element
    # ( image, threshold, max_value, threshold_type )
    ret, thresholded_img = cv2.threshold(
        img, threshold, 255, cv2.THRESH_BINARY)

    # return thresholded image
    return thresholded_img
