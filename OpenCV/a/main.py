import cv2
import image_operations as img_op
import image_filtering as img_fill
import image_convertions as img_conv


# read image into img variable
img = img_op.read_image('image.png')

# crop image
cropped_img = img_conv.crop_image(img, 10, 100, 10, 100)

# show cropped image
img_op.show_image(cropped_img)