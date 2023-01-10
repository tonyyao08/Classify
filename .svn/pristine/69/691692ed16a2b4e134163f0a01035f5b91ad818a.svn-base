import boto3


# pass in your IAM user aws keys
session = boto3.Session(
    aws_access_key_id="AKIAYN2NMRAHXCF5XFXA",
    aws_secret_access_key="1EelYhaBiLjN52OKdiHBK6cJ1PQ8rf0q9iN983/a",
)
# use the session to get the resource
s3 = session.resource("s3")

def retrieve_files(bucket_name):
    files = []
    my_bucket = s3.Bucket(bucket_name)
    for my_bucket_object in my_bucket.objects.all():
        files.append(my_bucket_object.key)
    return files

# s3 bucket name
bucket_name = "mycoins"

# example call to get all image file names from an s3 bucket
print(retrieve_files(bucket_name))
