# written in top-down design approach
import boto3
import json
import requests
from fuzzywuzzy import fuzz
from datetime import datetime


# hard-coded fields created from aws
bucket_name = "mycoins"
api_key = "da2-tkzuvhzfe5etrmisvfchmr7sia"
url = 'https://ztgryu55q5hs3o6tff5lh3qovq.appsync-api.us-east-1.amazonaws.com/graphql'


# intialize clients to communicate with aws services
s3 = boto3.client('s3')
rekognition = boto3.client("rekognition")


###########################################################################
# run train handler to retrieve updated fields from training


def handler(image_path, project_id):
    print("backend handler start time: " + datetime.now())
    # local label database unique to each project
    label_database = project_id + "-label.json"
    train_handler(project_id, label_database)
    classify_handler(image_path, project_id, label_database)

###########################################################################
# update our local labels database from webapp prior to classification


def train_handler(project_id, label_database):
    # use project id to get these bucket items from below query
    bucket_items = """\n    items {
        label
        rekognitionMeta
        }
    }
    }
    """
    query_bucket_items = ("query {\n" +
                          "  listImages(filter: {userGenerated: {eq: true}, projectID: {eq: \"" +
                          project_id + "\"}}) { ") + bucket_items

    bucket_data = run_query(query_bucket_items, api_key, url)
    user_labels = bucket_data.get("data").get("listImages")
    with open(label_database, 'w') as f:
        json.dump(user_labels, f, indent=4)
    print("BACKEND RETRIEVE LABELS END TIME: " + datetime.now())

###########################################################################
# helper function to run a post query request


def run_query(query, api_key, url):
    data = {"query": query}
    json_data = json.dumps(data)
    header = {"X-API-Key": api_key}

    response = requests.post(url=url, headers=header, data=json_data)
    return json.loads(response.text)

# detect text from images, try matching to labels and place images in a bucket
###########################################################################


def classify_handler(image_path, project_id, label_database):
    # get image name from full image path given
    image_name = image_path.rsplit('/', 1)[1]
    flipped_image_name = image_name.split('.')[0] + "_flipped.jpg"

    # detect text for both images, merge them into all detected text
    original_detected_text = detect_text(image_name, bucket_name)
    flipped_detected_text = detect_text(flipped_image_name, bucket_name)
    all_detected_text = original_detected_text + flipped_detected_text

    # check if detected text matches an existing label
    try:
        with open(label_database) as lf:
            labels_list = json.load(lf)
        map_image_to_label(all_detected_text, image_name,
                           labels_list, project_id)
        print("BACKEND MAP IMAGE END TIME: " + datetime.now())
    except Exception as e:
        print(e)

###########################################################################
# Utility functions for performming ML/database operations below
# upload an image to our s3 bucket


def upload_to_s3(image_path, image_name):
    try:
        s3.upload_file(image_path, bucket_name, image_name)
    except Exception as e:
        print(e)

###########################################################################
# detect text from a given image


def detect_text(photo, s3_bucket):
    response = rekognition.detect_text(
        Image={"S3Object": {"Bucket": s3_bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    text_arr = []
    for text in textDetections:
        # only include text with over 75% confidence level
        if (text["Confidence"]) > 75:
            text_arr.append(text["DetectedText"])

    return text_arr

###########################################################################
# check if an images detected text can be mapped to a label/bucket


def map_image_to_label(detect_text_response, image_name, labels_list, project_id):
    labels = labels_list.get("items")
    # call helper function to find best matching label for detected text
    label_name = get_matched_label(labels, detect_text_response)
    # update webapp with image and new label
    print(f"Classified {image_name} as {label_name}")
    create_image_query = send_web_image_classification_query(
        image_name, project_id, label_name, "false")

    data = {"query": create_image_query}
    json_data = json.dumps(data)
    header = {'X-API-Key': api_key}
    requests.post(url=url, headers=header, data=json_data)

###########################################################################
# look through all label-keyword pairs in database
# if we find a keyword that perfectly matches detected text, return label
# otherwise, keep track of current highest accuracy and label
# return this current highest label in the end if its accuracy > 60%
# otherwise, return unknown


def get_matched_label(labels, detect_text_response):
    current_best = "Unknown"
    highest_accuracy = 0
    for entry in labels:
        user_keywords_arr = entry.get("rekognitionMeta")
        for keyword in user_keywords_arr:
            for detected_text in detect_text_response:
                keyword = keyword.upper()
                # matches whole string accuracy
                f1 = fuzz.ratio(keyword, detected_text)
                if f1 == 100:
                    return entry.get("name")
                if highest_accuracy < f1:
                    highest_accuracy = f1
                    current_best = entry.get("name")
                # rearranges string into tokens, sorts and compares whole string
                f3 = fuzz.token_sort_ratio(keyword, detected_text)
                if f3 == 100:
                    return(entry.get("name"))
                if highest_accuracy < f3:
                    highest_accuracy = f3
                    current_best = entry.get("name")
                if highest_accuracy > 60:
                    return current_best
                else:
                    return "Unknown"

##########################################################################
# generate the query that is sent back to the web app


def send_web_image_classification_query(image_name, proj_id, label_name, user_generated):
    create_image_query = f"""mutation {{ 
            createImage(input: {{imageKey: "{image_name}", projectID: "{proj_id}", label: "{label_name}", userGenerated: {user_generated}}}) {{ 
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
            }}"""
    return create_image_query
