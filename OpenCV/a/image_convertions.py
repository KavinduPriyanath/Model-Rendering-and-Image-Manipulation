
import cv2
import numpy as np


def translate_image(img, _x, _y):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # check whether _x and _y are integers
    if type(_x) != int or type(_y) != int:
        raise TypeError('_x and _y must be integers')

    # translation matrix
    # [ 1 0 _x ]
    # [ 0 1 _y ]
    translation_matrix = np.float32([[1, 0, _x], [0, 1, _y]])

    # translate image
    # warpAffine -> applies affine transformation to an image
    # ( image, translation_matrix, (width, height) )
    translated_img = cv2.warpAffine(
        img, translation_matrix, (img.shape[1], img.shape[0]))

    # return translated image
    return translated_img


def rotate_image(img, angle):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # check whether angle is an integer
    if type(angle) != int:
        raise TypeError('angle must be an integer')

    # rotation matrix
    # [ cos(angle) -sin(angle) ]
    # [ sin(angle)  cos(angle) ]
    # getRotationMatrix2D -> returns a rotation matrix for a specified angle
    # ( (width/2, height/2), angle, scale )
    rotation_matrix = cv2.getRotationMatrix2D(
        (img.shape[1]/2, img.shape[0]/2), angle, 1)

    # rotate image
    # warpAffine -> applies affine transformation to an image
    # ( image, rotation_matrix, (width, height) )
    rotated_img = cv2.warpAffine(
        img, rotation_matrix, (img.shape[1], img.shape[0]))

    # return rotated image
    return rotated_img


def scale_image(img, scale):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # check whether scale is a float
    if type(scale) != float:
        raise TypeError('scale must be a float')

    # check whether scale is not 0
    if scale == 0:
        raise ValueError('scale cannot be 0')

    # scale image
    # resize -> resizes an image
    # ( image, (width, height), x_scale, y_scale )
    scaled_img = cv2.resize(img, None, fx=scale, fy=scale)

    # another way to scale image
    #   scaled_img = cv2.resize( img, (int(img.shape[1]*scale), int(img.shape[0]*scale)) )

    # return scaled image
    return scaled_img


def shear_image(img, _x_factor, _y_factor):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # check whether _x_factor and _y_factor are integers
    if type(_x_factor) != int or type(_y_factor) != int:
        raise TypeError('_x_factor and _y_factor must be integers')

    # shear matrix
    # [ 1 _x_factor  0 ]
    # [ _y_factor 1  0 ]
    shear_matrix = np.float32([[1, _x_factor, 0], [_y_factor, 1, 0]])

    # shear image
    # warpAffine -> applies affine transformation to an image
    # ( image, shear_matrix, (width, height) )
    sheared_img = cv2.warpAffine(
        img, shear_matrix, (img.shape[1], img.shape[0]))

    # return sheared image
    return sheared_img


def horizontal_reflection(img):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # horizontal reflection matrix
    # [ -1 0 width ]
    # [ 0 1 0 ]
    horizontal_reflection_matrix = np.float32(
        [[-1, 0, img.shape[1]], [0, 1, 0]])

    # horizontal reflection
    # warpAffine -> applies affine transformation to an image
    # ( image, horizontal_reflection_matrix, (width, height) )
    horizontal_reflected_img = cv2.warpAffine(
        img, horizontal_reflection_matrix, (img.shape[1], img.shape[0]))

    # return horizontal reflected image
    return horizontal_reflected_img


def vertical_reflection(img):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # vertical reflection matrix
    # [ 1 0 0 ]
    # [ 0 -1 height ]
    vertical_reflection_matrix = np.float32([[1, 0, 0], [0, -1, img.shape[0]]])

    # vertical reflection
    # warpAffine -> applies affine transformation to an image
    # ( image, vertical_reflection_matrix, (width, height) )
    vertical_reflected_img = cv2.warpAffine(
        img, vertical_reflection_matrix, (img.shape[1], img.shape[0]))

    # return vertical reflected image
    return vertical_reflected_img


def horizontal_and_vertical_reflection(img):

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    # horizontal and vertical reflection matrix
    # [ -1 0 width ]
    # [ 0 -1 height ]
    horizontal_and_vertical_reflection_matrix = np.float32(
        [[-1, 0, img.shape[1]], [0, -1, img.shape[0]]])

    # horizontal and vertical reflection
    # warpAffine -> applies affine transformation to an image
    # ( image, horizontal_and_vertical_reflection_matrix, (width, height) )
    horizontal_and_vertical_reflected_img = cv2.warpAffine(
        img, horizontal_and_vertical_reflection_matrix, (img.shape[1], img.shape[0]))
    
    # can use both above defined functions
    # horizontal_and_vertical_reflected_img = horizontal_reflection( vertical_reflection( img ) )

    # return horizontal and vertical reflected image
    return horizontal_and_vertical_reflected_img

def crop_image(img, left, right, top, bottom) :

    # check whether img is a numpy array
    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')
    
    # check whether right, left, top, bottom are integers
    if type(right) != int or type(left) != int or type(top) != int or type(bottom) != int:
        raise TypeError('right, left, top, bottom must be integers')
    
    # check whether right, left, top, bottom are not negative
    if right < 0 or left < 0 or top < 0 or bottom < 0:
        raise ValueError('right, left, top, bottom cannot be negative')
    
    # check whether right, left, top, bottom are not greater than image width and height
    if right > img.shape[1] or left > img.shape[1] or top > img.shape[0] or bottom > img.shape[0]:
        raise ValueError('right, left, top, bottom cannot be greater than image width and height')
    
    # check whether right is greater than left
    if right <= left:
        raise ValueError('right cannot be less than left')
    
    # check whether bottom is greater than top
    if bottom <= top:
        raise ValueError('bottom cannot be less than top')

    # crop image
    # using array slice
    # [ top : bottom, left : right ]
    cropped_img = img[top : bottom, left : right]

    # return cropped image
    return cropped_img