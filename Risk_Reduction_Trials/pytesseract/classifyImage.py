from pytesseract import pytesseract
import cv2
import numpy as np

# Tutorial link here: https://nanonets.com/blog/ocr-with-tesseract/

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


image = cv2.imread("GeorgiaQuarter.jpg")
image2 = cv2.imread("GeorgiaQuarterRotated.jpg")

gray1 = get_grayscale(image)
thresholding1 = thresholding(gray1)

gray2 = get_grayscale(image2)
thresholding2 = thresholding(gray2)

# Adding custom options
custom_config = (
    r"--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPAQRSTUVWXYZ"
)

print(pytesseract.image_to_string(thresholding1, lang="eng", config=custom_config))
print("----------------------------------------------------------------------")
print(pytesseract.image_to_string(thresholding2, lang="eng", config=custom_config))
