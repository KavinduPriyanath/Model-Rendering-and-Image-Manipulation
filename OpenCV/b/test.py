import cv2
import pytesseract
import numpy as np
import easyocr
import keras_ocr as kocr
import matplotlib.pyplot as plt

# read image into img variable
img = cv2.imread('license_plate.jpeg')

# convert image to grayscale
gray_scaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply bilateral filter
# bilateral filter -> removes noise from image
gray_scaled = cv2.bilateralFilter(gray_scaled, 15, 20, 20)

# apply canny edge detection
# canny edge detection -> detects edges in image
# ( image, lower_threshold, upper_threshold )
edges = cv2.Canny(gray_scaled, 170, 200)

# show edged image
cv2.imshow("Edged", edges)
cv2.waitKey(0)

# find contours
# contours are the boundaries of an object
# RETR_LIST -> retrieves all contours
# CHAIN_APPROX_SIMPLE -> removes all redundant points and compresses the contour
# ( image, mode, method )
contours, heirarchy = cv2.findContours(
    edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# make a copy of original image
img1 = img.copy()

# draw all contours on the copy of original image
# ( image, contours, contour_index, color, thickness )
cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)

# show all contours
cv2.imshow("All of the contours", img1)
cv2.waitKey(0)

# Contours are basically the curves that join all the continuous points having the same intensity or color

# sort contours based on area
# and take top 30 contours
# sorted -> sorts the elements of a given iterable in a specific order
# ( iterable, key, reverse )
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

# initialize Number Plate contour
Number_Plate_Contour = 0

# loop over contours
# to find the contour with 4 points -> rectangular shape
for current_contour in contours:

    # approximate the contour
    # arcLength -> calculates the contour perimeter or a curve length
    # ( contour, closed )
    perimeter = cv2.arcLength(current_contour, True)

    # approxPolyDP -> approximates a polygonal curve with the specified precision
    # ( contour, epsilon, closed )
    # (current contour, maximum distance from contour to approximated contour, True)
    approx = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)

    # check if approximated contour has 4 points
    if len(approx) == 4:
        Number_Plate_Contour = approx
        break

# A mask is a binary image consisting of zero- and non-zero values. If a mask is applied to another binary or to a grayscale image of the same size, all pixels which are zero in the mask are set to zero in the output image.

# initialize mask with zeros of same shape as gray_scaled
mask = np.zeros(gray_scaled.shape, np.uint8)

# draw contour on mask
# ( image, contours, contour_index, color, thickness )
new_image1 = cv2.drawContours(mask, [Number_Plate_Contour], 0, 255, -1,)

# apply bitwise_and operation
# bitwise_and -> computes bitwise conjunction of two arrays
# ( src1, src2, mask )
new_image1 = cv2.bitwise_and(img, img, mask=mask)

# show Number Plate
cv2.imshow("Number Plate", new_image1)
cv2.waitKey(0)

# convert image to grayscale
gray_scaled1 = cv2.cvtColor(new_image1, cv2.COLOR_BGR2GRAY)

# apply threshold
# threshold -> applies fixed-level threshold to each array element
# ( image, threshold, max_value, threshold_type )
ret, processed_img = cv2.threshold(
    np.array(gray_scaled1), 125, 255, cv2.THRESH_BINARY)

# show processed image
cv2.imshow("Number Plate", processed_img)
cv2.waitKey(0)

# recognize text from image
# image_to_string -> returns result as string
# text = pytesseract.image_to_string(processed_img, lang='eng')
# print("Number is :", text)
# cv2.waitKey(0)

easyocr_reader = easyocr.Reader(["en"])

result = easyocr_reader.readtext(processed_img)

for (bbox, text, prob) in result :

    print(f'{text} ({prob})')

# pipeline = kocr.pipeline.Pipeline()


# prediction_groups = pipeline.recognize([img])

# fig, axs = plt.subplots(nrows=len(img), figsize=(10, 20))
# for ax, image, predictions in zip(axs, img, prediction_groups):
#     kocr.tools.drawAnnotations(image=image, 
#                                     predictions=predictions, 
#                                     ax=ax)

# cv2.imshow("Number Plate", img)
# cv2.waitKey(0)
