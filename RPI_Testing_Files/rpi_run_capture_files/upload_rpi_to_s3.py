import boto3
from PIL import Image
from datetime import datetime


def upload_image(parent_path,image_name, bucket,in_bucket_prefix):

    # Upload the file
    s3_client = boto3.client('s3')

    flipped_image_name = flip_image(parent_path,image_name)
    print(datetime.now()) 
    try:
        response = s3_client.upload_file(parent_path+image_name, bucket, in_bucket_prefix+image_name)
        print(response)
        print(datetime.now()) 
        response = s3_client.upload_file(parent_path+flipped_image_name, bucket, in_bucket_prefix + flipped_image_name)
        print(response)
        print(datetime.now()) 
        
    except Exception as e:
        print(e)
        return False
    
    return True

def flip_image(parent_path,img_name):
    # open the original image
    original_img = Image.open(parent_path + img_name)
    # rotate original image 180 degrees
    vertical_img = original_img.rotate(180)
    # create a new file name for the flipped image and save it
    flipped_image_name = img_name.split('.')[0] + "_flipped.jpg"
    vertical_img.save(parent_path+flipped_image_name)
    
    # close all our files object
    original_img.close()
    vertical_img.close()
    return flipped_image_name


#Driver
# parent_path = "/home/pi/Desktop/local_images/"
# img_name = "newyork_quarter.jpg"
# bucket = "aal-rpi-bucket"
# in_bucket_prefix = "test_images/"
# print(upload_image(parent_path,img_name, bucket,in_bucket_prefix))
