import cv2
import numpy as np


def read_image(image_path):

    if type(image_path) != str:
        raise TypeError('image_path must be a string')

    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError('image_path does not exist')

    return img


def show_image(img):

    if type(img) != np.ndarray:
        raise TypeError('img must be a numpy array')

    cv2.imshow('image', img)

    while True:
        key_pressed = cv2.waitKey(0)

        if key_pressed == 27:
            break

    cv2.destroyAllWindows()
