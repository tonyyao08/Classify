import boto3
from PIL import Image


def upload_image(file_name, bucket):

    # Upload the file
    s3_client = boto3.client('s3')

    flipped_image_name = flip_image(file_name)
    try:
        response = s3_client.upload_file(flipped_image_name, bucket, flipped_image_name)
        print(response)
    except Exception as e:
        print(e)
        return False
    return True

def flip_image(file_name):
    # open the original image
    original_img = Image.open(file_name)
    # rotate original image 180 degrees
    vertical_img = original_img.rotate(180)
    # create a new file name for the flipped image and save it
    flipped_image_name = file_name.split('.')[0] + "_flipped.jpg"
    vertical_img.save(flipped_image_name)
    
    # close all our files object
    original_img.close()
    vertical_img.close()
    return flipped_image_name

print(upload_image("newyork-quarter.jpg", "mycoins" ))