from communicator import Communicator
from classifier import Classifier
from detector import Detector
from camera import Camera
from processor import Processor
from GUI import display_gui
import RPi.GPIO as GPIO
import PySimpleGUI as sg
import sys
import logging
from datetime import datetime
import cv2


def main():
    startTime = datetime.now().strftime("%B_%d_%H:%M")
    logging.basicConfig(level=logging.INFO, filename=f"logs/{startTime}.log",
                        filemode="w", format='%(asctime)s - %(message)s')
    ledPin = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ledPin, GPIO.OUT)
    camera = Camera()
    communicator = Communicator()
    try:
        projects = communicator.getAvailableProjects()
        projects = list(
            map(lambda project: project.get("projectName"), projects))
        selectedProject = display_gui(projects)
        communicator.setCurrentProjectByName(selectedProject)

        classifier = Classifier(communicator)
        detector = Detector()
        processor = Processor()

        for frame in camera.getFrame():
            camera.reset()
            frame = frame.array
            GPIO.output(ledPin, GPIO.LOW)
            if communicator.getProjectMode() is None:
                logging.error("NO PROJECT SET WHILE CAPTURING")
            elif communicator.getProjectMode() == "TRAIN":
                if detector.doCapture(frame):
                    GPIO.output(ledPin, GPIO.HIGH)
                    logging.info("BEGIN IMAGE PRE-PROCESSING")
                    image = processor.process(frame)
                    logging.info("END IMAGE PRE-PROCESSING")
                    classifier.addTrainingImage(image)
                    GPIO.output(ledPin, GPIO.LOW)
            elif communicator.getProjectMode() == "CLASSIFY":
                if detector.doCapture(frame):
                    GPIO.output(ledPin, GPIO.HIGH)
                    logging.info("BEGIN IMAGE PRE-PROCESSING")
                    image = processor.process(frame)
                    logging.info("END IMAGE PRE-PROCESSING")
                    classifier.addClassifyImage(image)
                    GPIO.output(ledPin, GPIO.LOW)

            # exitkey = cv2.waitKey(2)
            # if exitkey == 27:
            #     GPIO.output(ledPin, GPIO.LOW)
            #     cv2. destroyAllWindows()
            #     communicator.destroy()
            #     sys.exit(0)

    except KeyboardInterrupt:
        GPIO.output(ledPin, GPIO.LOW)
        communicator.destroy()
        sys.exit(0)


if __name__ == "__main__":
    main()
