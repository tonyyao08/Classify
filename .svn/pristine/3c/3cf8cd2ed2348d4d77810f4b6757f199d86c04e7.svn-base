# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3


def detect_text(photo, s3_bucket):
    client = boto3.client("rekognition")
    response = client.detect_text(Image = {"S3Object": {"Bucket": s3_bucket, "Name": photo}})
    textDetections = response["TextDetections"]
    text_arr = []
    for text in textDetections:
        # only include text with over 75% confidence level
        if (text["Confidence"]) > 75:
            text_arr.append(text["DetectedText"])
    
    return text_arr


# s3 bucket name
s3_bucket = "mycoins" 
# photo name as stored in s3 bucket
photo = "newyork-quarter1.jpg" 

# example call to view all text detected
text_arr = detect_text(photo, s3_bucket)
print(text_arr)

