# Sanjay Sharma, CMSC435 Sec. 0101
# Obj: Try to see how we can interface Raspberry Pi 3B with AWS
 
import boto3

client = boto3.client('s3', region_name='us-east-1')

# make your own account, uploading it to my own bucket

client.upload_file('images/image_0.jpg', 'mybucket', 'image_0.jpg')
