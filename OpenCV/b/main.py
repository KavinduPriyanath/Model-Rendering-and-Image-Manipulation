import cv2
import easyocr

# initialize easyocr reader
#
easyocr_reader = easyocr.Reader(['en'])

# read image into img variable
img = cv2.imread('license_plate.jpeg')

# initialize haar cascade classifier
plate_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# convert image to binary
_, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

# detect plates in image
plates = plate_cascade.detectMultiScale(
    gray, scaleFactor=1.2, minNeighbors=5, minSize=(25, 25))

# loop over detected plates
for (x, y, w, h) in plates:

    # draw rectangle around plate
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # crop plate from image
    cropped_plate = img[y:y + h, x:x + w]

    # convert cropped plate to grayscale
    _, binary_plate = cv2.threshold(
        cropped_plate, 0, 255, cv2.THRESH_BINARY)

    # recognize text from plate
    result = easyocr_reader.readtext(cropped_plate)

    # loop over results
    for (bbox, text, prob) in result:
            
        # display text and probability
        print(f'{text} ({prob})')

# show image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

