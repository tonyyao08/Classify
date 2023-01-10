# written in top-down design approach
import boto3
import json
from PIL import Image
from os.path import exists

bucket_name = "mycoins" # hard-coded
# retrieve from amplify request
project_name = "my-third-project"
# retrieve from amplify request
train_mode = False
s3 = boto3.client('s3')
rekognition = boto3.client("rekognition")
label_database = project_name + "-label.json"
bucket_database = project_name + "-bucket.json"

# on startup, create database to store user created labels and matched buckets
def initalize_databases(label_database, bucket_database):
    empty_json = []
    with open(label_database, 'w') as f:
        json.dump(empty_json, f, indent=4)

    with open(bucket_database, 'w') as f:
        json.dump(empty_json, f, indent=4)


# TRAINING MODE: users add labels to help recongnize images based off text
def train_handler():
    user_entered_label = "West Virginia"
    user_entered_text = ["West", "Virginia"]
    add_label(label_database, user_entered_label, user_entered_text)
    print("added text to identify this image to label database")

# CLASSIFY MODE: detect text from images and place in bucket
def classify_handler():
    # upload original image taken to s3 bucket
    image_file = "April_19_2022_22:33:02.jpg"
    parent_path = "/home/pi/Desktop/local_images/"
    upload_to_s3(parent_path,image_file)
    # upload original image rotated 180 degrees to s3 bucket
    flipped_image_file = flip_image(parent_path,image_file)
    upload_to_s3(parent_path,flipped_image_file)

    # detect text for both images, merge them into all detected text
    original_detected_text = detect_text(image_file, bucket_name)
    print("ORIGINAL:")
    print(original_detected_text)
    flipped_detected_text = detect_text(flipped_image_file, bucket_name)
    print("FLIPPED:")
    print(flipped_detected_text)
    all_detected_text = original_detected_text + flipped_detected_text
    print("ALL:")
    print(all_detected_text)
    
    # check if detected text matches an existing label
    try:
        map_image_to_label(all_detected_text, image_file, label_database, bucket_database)
        print("placed image into a bucket")
    except Exception as e:
        print(e)


# Utility functions for performming ML/database operations below


# upload an image to our s3 bucket
def upload_to_s3(parent_path,image_file):
    try:
        response = s3.upload_file(parent_path + image_file, bucket_name, image_file)
        print(response)
    except Exception as e:
        print(e)


# flip an image by 180 degrees
def flip_image(parent_path,file_name):
    # open the original image
    original_img = Image.open(parent_path+file_name)
    # rotate original image 180 degrees
    vertical_img = original_img.rotate(180)
    # create a new file name for the flipped image and save it
    flipped_image_name = file_name.split('.')[0] + "-flipped.jpg"
    vertical_img.save(parent_path+flipped_image_name)
    
    # close all our files object
    original_img.close()
    vertical_img.close()
    return flipped_image_name


# detect text from a given image
def detect_text(photo, s3_bucket):
    response = rekognition.detect_text(Image = {"S3Object": {"Bucket": s3_bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    text_arr = []
    for text in textDetections:
        # only include text with over 75% confidence level
        if (text["Confidence"]) > 75:
            text_arr.append(text["DetectedText"])
    
    return text_arr


# check if an images detected text can be mapped to a label/bucket
def map_image_to_label(detect_text_response, image_file, label_database, bucket_database):
    with open(label_database) as lf:
        labels_list = json.load(lf)

    with open(bucket_database) as pf:
        prev_database = json.load(pf)

    name = "Unknown"
    labels = [d['label'] for d in labels_list]
    for entry in labels:
        user_text_arr = entry.get("matchingText")
        for user_text in user_text_arr:
            for detected_text in detect_text_response:
                # call our own function used for matching similar text
                if match_text(user_text.upper(), detected_text):
                    name = entry.get("name")

    new_bucket = {image_file:name}
    prev_database.append(new_bucket)
    
    with open(bucket_database, 'w', encoding='utf-8') as f:
        json.dump(prev_database, f, indent=4)

# match similar words to allow for one off errors based off word length
def match_text(s1, s2):
    if s1 == s2:
        return True
    else:
        # convert words to char array to check for one off errors
        char_array1 = [char for char in s1]
        char_array2 = [char for char in s2]
        # get smallest and biggest length
        l1 = len(char_array1)
        l2 = len(char_array2)
        min_length = l1 if l1 < l2 else l2
        max_length = l1 if l1 > l2 else l2
        # initalize number of mismatched chars to difference between lengths 
        mismatch_count = max_length - min_length
        # accept one or more errors for words with > 2 characters
        if min_length < 3:
            return False
        return close_enough(char_array1, char_array2, min_length, mismatch_count)

# check if 2 words are close enough to be counted as the same
def close_enough(c1, c2, min_length, mismatch_count):
    # count occurences of mismatched characters
    for i in range(min_length):
        if c1[i] != c2[i]:
            mismatch_count+=1
    # accept 1 mismatch for words with length < 5
    if min_length < 5:
        return True if mismatch_count <= 1 else False
    else: # accept 2 mismatches for words with length >= 5
        return True if mismatch_count <= 2 else False

# add user inputed label and text into local json file
def add_label(label_database, label_name, matching_text):
    with open(label_database) as pf:
        prev_database = json.load(pf)

    new_label = {"label": {"name": label_name, "matchingText": matching_text}}
    prev_database.append(new_label)
    with open(label_database, 'w') as f:
        json.dump(prev_database, f, indent=4)


# if database doesn't exist, create databases
if exists(label_database) == False:
    initalize_databases(label_database, bucket_database)

# run train or classify mode
if train_mode:
    train_handler()
else:
    classify_handler()