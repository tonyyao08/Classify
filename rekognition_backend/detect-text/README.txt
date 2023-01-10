TO ACCESS MY DATABASE, FOLLOW STEPS BELOW

1. install amazon cli

2. run aws configure, enter the following fields below
    2.1. For AWS Access Key ID: 
        AKIAYN2NMRAHXCF5XFXA 
    2.2. For AWS Secret Access Key: 
        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   
    2.3. For Default region name:
        us-east-1
    2.4. For Default output format:
        json

3. pip install boto3 to connect to aws client


detect_text.py uses AmazonRekognition to return all detected text from an image stored in an s3 bucket


add_label.py demonstrates how users can add their labels to a database and have python create buckets with these labels


map_image_to_label.py demonstrates how the detected text from images can be placed into buckets and stored in a database


retrieve_files.py utility used to get all file names from a specified s3 bucket


upload_image.py utility used to rotate a given image by 180 degrees and 
upload the new image back into S3 bucket, to process text for rotated images


create_bucket.py is used to create a bucket whenever a project is created,
and enforces the s3 bucket naming convention by just adding "-bucket"
to the project name which is created with valid naming conventions


match_text.py utility used to help identify words that may have been detected as different, but are actually close enough to a word the user supplied to be 
considered as the same


Note: s3 images are retrieved from my aws accounts s3 bucket, referenced here for devs to view what's currently in my bucket 


Databases represented in json currently. Users can add their own labels to the database by supplying a label name and matching text that can help identify the label. Then an image is mapped to a label based off this matching text and the text detected from the image. 


TODO: allow user to input fields, create GUI?
