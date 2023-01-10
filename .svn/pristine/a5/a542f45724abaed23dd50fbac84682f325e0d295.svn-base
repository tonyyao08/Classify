import cv2
from datetime import datetime
from image import Image
import logging

# This is the image processing class. After the camera has taken an
# image, we perform some processing on it with the final image that
# being shown to the user. The supplementary images we construct from
# the original image are sent to the model so that text can be extracted
# from it and be used to classify it.


class Processor:
    def __init__(self):
        self.localPath = "/home/pi/Desktop/local_images/"

    def process(self, frame, isTraining=False):
        """
        Save the brightness adjusted image and add the rotated images.
        """
        frame = self.crop(frame)
        frame = self.brightness_contrast(frame, 10, 30)
        image = Image(frame)
        if not isTraining:
            image.addNamedVersion("90", self.rotate90(frame))
            image.addNamedVersion("180", self.rotate180(frame))
            image.addNamedVersion("270", self.rotate270(frame))
        return image

    def crop(self, frame):
        """
        Crop the frame to only include the area of the coin. This also
        standardizes the image size.
        """
        (height, width, _) = frame.shape
        y_buff = int(height*.024)
        x_buff = int(width*.15)
        return frame[y_buff:height-y_buff, x_buff:width-x_buff]

    def rotate90(self, frame):
        """
        Rotate the image by 90 degrees and return the rotated image.
        """
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    def rotate180(self, frame):
        """
        Rotate the image by 180 degrees and return the rotated image.
        """
        return cv2.rotate(frame, cv2.ROTATE_180)

    def rotate270(self, frame):
        """
        Rotate the image by 270 degrees and return the rotated image.
        """
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def get_new_filename(self, local_img_folder):
        """
        The naming convention we utilize to name images, is based on 
        the date and time the image was taken.Each image is given the 
        filename in the format of for ex. "May_1_19:20:22"
        """
        now = datetime.now()
        image_name = now.strftime("%B_%d_%H:%M:%S")
        return (local_img_folder+image_name, image_name)

    def brightness_contrast(self, img, b, c):
        """
        This function adjusts the brighntess and contrast of an image
        so that we can get a better quality image to put into the model.
        """
        brightness = 255 + b
        contrast = 127 + c
        brightness = int((brightness - 0) *
                         (255 - (-255)) / (510 - 0) + (-255))
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                max = 255
            else:
                shadow = 0
                max = 255 + brightness
            al_pha = (max - shadow) / 255
            ga_mma = shadow
            cal = cv2.addWeighted(img, al_pha,
                                  img, 0, ga_mma)
        else:
            cal = img
        if contrast != 0:
            Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            Gamma = 127 * (1 - Alpha)

            cal = cv2.addWeighted(cal, Alpha,
                                  cal, 0, Gamma)
        return cal
