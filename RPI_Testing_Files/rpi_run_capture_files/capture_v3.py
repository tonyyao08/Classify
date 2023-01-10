# THIS CODE WILL TAKE PICTURES USING THE CAMERA
# CLICK ON THE FRAME AND PRESS THE "K" KEY TO TAKE A PICTURE
# CLICK ON THE FRAME AND PRESS THE "ESC" KEY TO EXIT
# PICTURES ARE SAVED AS IMAGE.JPG

# run this
# sudo apt-get update && sudo apt-get install python3-gpiozero python-gpiozero
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import cv2
import time
from picamera.array import PiRGBArray
from datetime import datetime
from upload_rpi_to_s3 import *
from backend_handler import *
import RPi.GPIO as GPIO
import json
import requests
import numpy as np
from contrast import *
import os

# if train = true, then train mode


def conveyor_belt(bucket, in_bucket_prefix, num_objects, path_for_local_imgs, train, projID):
    # Set up LED
    led = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(led, GPIO.OUT)

    # Setup camera
    camera = PiCamera()
    res = (1920, 1088)
    camera.resolution = (1920, 1088)
    camera.framerate = 120
    rawCapture = PiRGBArray(camera, size=res)
    time.sleep(.1)
    # cap = cv2.VideoCapture(0)  # camera input
    local_img_folder = path_for_local_imgs
    interval = 2
    start_time = time.time()
    taken = 0
    lower = 120

    # S3 information:
    parent_path = local_img_folder
    # in_bucket_prefix = ""
    b = 1
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        original_image = frame.array
        image = original_image
        h_i, w_i, _ = image.shape

        # resize window
        rs = .78
        window_width = int(w_i * rs)
        window_height = int(h_i * rs)
        cv2.namedWindow('section', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('section', window_width, window_height)

        # We have the image so we can perform some processing on it
        y_buffer = 45
        x_scale = 5
        ymin = y_buffer
        ymax = h_i - y_buffer
        xmin = int(w_i/x_scale)
        xmax = int(w_i - xmin)

        # Width and Height
        w_x = xmax - xmin
        h_y = ymax - ymin
        cv2.rectangle(image, (xmin, ymin),
                      (xmin + w_x, ymin + h_y), (255, 0, 0), 5)

        # Bounding Box
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.rectangle(image, (xmin, ymin),
                      (xmin + w_x, ymin + h_y), (255, 0, 0), 5)
        # If its really Bright, increase to 150
        # If its Dark drop to 100

        #thresh_img = highlight_object(image)
        key = cv2.waitKey(30)
        if key == 108:
            lower -= 5
            print(lower)
        if key == 107:
            lower += 5
            print(lower)
        _, thresh_img = cv2.threshold(
            gray_image, lower, 255, cv2.THRESH_BINARY)
       # Get contours
        contours, _ = cv2.findContours(
            thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get the largest contour
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_cnt = cnt
                max_area = area

        # If statement to display Video Feed
        if max_area > 20000:
            (x, y, w, h) = cv2.boundingRect(max_cnt)
            tup = (x, y, w, h)
            #area = cv2.contourArea(max_cnt)
            if ((xmin <= x) and (x+w <= xmax) and (ymin <= y) and (y+h <= ymax)):
                # Put a rectangle around the object
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.putText(image, f"{max_area}  x = {x}",
                            (x, y-15), 1, 1, (0, 255, 0))

        #image = sharpen(image)
        cv2.namedWindow('section', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('section', window_width, window_height)

        cv2.imshow('section', image)

        if key == 99 and time.time() - start_time >= interval:
            # Turn the led on
            GPIO.output(led, GPIO.HIGH)

            # Get img save path and image name
            img_save_path, image_name = get_new_filename(local_img_folder)

            # Capture image
            camera.capture(img_save_path)
            print(f"Image {image_name} saved")
            print(datetime.now())

            # Crop image and save
            cropped = crop(img_save_path, 20)
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
#             cropped = sharpen(cropped,2)
            #cv2.imwrite(img_save_path, cropped)
            contrast = brightness_contrast(cropped, b=0, c=40)
            cv2.imwrite(img_save_path, contrast)

            # Here we send to s3
            upload_image(parent_path, image_name+".jpg",
                         bucket, in_bucket_prefix)
            taken += 1
            apiKey = "da2-tkzuvhzfe5etrmisvfchmr7sia"
            #projID = "2a478f48-2a93-4501-9627-bcad74587cf5"
            if train:
                # Create Image Query
                create_image_query = gen_web_image_query(image_name, projID)

                url = 'https://ztgryu55q5hs3o6tff5lh3qovq.appsync-api.us-east-1.amazonaws.com/graphql'

                data = {"query": create_image_query}
                json_data = json.dumps(data)
                header = {'X-API-Key': apiKey}
                requests.post(url=url, headers=header, data=json_data)
                # END TONYS CODE
            else:
                # run backend handler, need to pass in the image path and project id
                handler(img_save_path, projID)

            start_time = time.time()
            GPIO.output(led, GPIO.LOW)

        # if escape key is hit then exit
        if key == 27 or taken >= int(num_objects):
            # print(create_image_query)
            GPIO.output(led, GPIO.LOW)

            break

        rawCapture.truncate(0)
#################################################################


def get_new_filename(local_img_folder):
    now = datetime.now()
    image_name = now.strftime("%B_%d_%H:%M:%S")
    return local_img_folder+image_name+".jpg", image_name
#################################################################


def crop(img_save_path, buffer):
    img = cv2.imread(img_save_path)
    # find object
    height, width, _ = img.shape
    # y_buff = int(height*.34) #roughly 130
    # x_buff = int(width*.4) #roughly 340
    y_buff = int(height*.035)
    x_buff = int(width*.17)
    # print(img.shape)
#     b = 20
#     img = img[max(0,y-b):min(y+h+b,height),max(0,x-b):min(x+w+b,width)]
    img = img[y_buff:height-y_buff, x_buff:width-x_buff]
    return img

#################################################################


def gen_web_image_query(image_name, projID):
    final_image = image_name + ".jpg"
    create_image_query = f"""mutation {{ 
            createImage(input: {{imageKey: "{final_image}", projectID: "{projID}"}}) {{ 
                id 
                _version
                createdAt
                updatedAt
                _lastChangedAt
                projectID
                _deleted
                imageKey
                label
                rekognitionMeta
                userGenerated
            }}
            }}"""  # .format(final_image = final_image, projID = projID)
    return create_image_query
###################################################################################


def make_folders(folder_names_list, parent_path):
    #folders = ["penny","nickel","dime","quarter","dollar","Unknown"]
    for f in folder_names_list:
        path = parent_path + str(f)
        try:
            os.mkdir(path)
        except OSError:
            print(f"Could not create {path}")
        else:
            print("Successfully created the directory %s " % path)
###################################################################################

#################################################################
# # # Driver
# bucket = "mycoins"
# in_bucket_prefix = ""
# path_for_local_imgs = "/home/pi/Desktop/local_images/"
# num_objects = 4

# conveyor_belt(bucket, in_bucket_prefix, num_objects,
#               path_for_local_imgs, True, "hello")
