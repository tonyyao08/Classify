import boto3


def upload_image(file_name, bucket):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, file_name)
    except Exception as e:
        print("failed to upload images: " + e)
    print("IMAGE WAS UPLOADED")

upload_image("07_contrast_10_40_rot2.jpg", "mycoins" )
print("EVERYTHING PASSED")