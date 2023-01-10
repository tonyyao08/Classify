from datetime import datetime
import cv2
import base64
import logging

# This is the Image class, where we create an object each time we handle an
# an image and its different versions.


class Image:
    localPath = "/home/pi/Desktop/local_images/"
    defaultExtension = ".jpeg"

    def __init__(self, frame):
        """
        Each image is now an object with its own key, image frame and 
        display option.
        """
        self.imageKey = datetime.now().strftime("%B_%d_%H:%M:%S")
        self.frame = frame
        self.originalVersion = ("original", frame)
        self.versions = [self.originalVersion]

    def writeToDisk(self, version=None):
        """
        Save the image to the the local disk so that it can be then sent to the s3 bucket
        """
        if version is None:
            for v in self.versions:
                (versionName, frame) = v
                cv2.imwrite(self.getFullPath(versionName), frame)
        else:
            v = self.getVersion(version)
            (versionName, frame) = v
            cv2.imwrite(self.getFullPath(versionName), frame)

    def base64encode(self):
        """
        Return the encoded value associated with a versioned image.
        """
        return list(map(lambda version: self.encodeVersion(version), self.versions))

    def encodeVersion(self, version):
        """
        Return the versionName and buffer image tuple associated with a specific version.
        """
        (versionName, frame) = version
        _, buffer = cv2.imencode(Image.defaultExtension, frame)
        return (versionName, buffer)

    def getFilename(self, version=None):
        """
        Return the filename associated with the current image. If no version 
        is given, we assume no version has been 
        """
        if version is None or version == "original":
            return self.imageKey + Image.defaultExtension
        else:
            return self.imageKey + "_" + version + Image.defaultExtension

    def getFullPath(self, version=None):
        """
        Return the full path of the image, specifying which image it is from.
        """
        return Image.localPath + self.getFilename(version)

    def getFrame(self, version=None):
        """
        Get the Frame of the current image and return it. Make sure to grab the
        correct version of the image.
        """
        if version is None or version == "original":
            return self.frame
        else:
            v = self.getVersion(version)
            (_, frame) = v
            return frame

    def getVersion(self, version=None):
        """
        Get the version of the current image since each image will have 4 versions
        that are being processed.
        """
        if version is None:
            return self.originalVersion
        else:
            return next(
                (x for x in self.versions if x[0] == version), self.originalVersion)

    def addNamedVersion(self, versionName, frame):
        """
        Add the version name to the current image's list of versions.
        """
        self.versions.append((versionName, frame))
