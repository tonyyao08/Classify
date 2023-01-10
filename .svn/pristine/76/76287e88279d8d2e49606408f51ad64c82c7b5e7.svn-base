import boto3

def create_bucket(project_name):
    
    # Create a bucket when a user creates a new project
    s3_client = boto3.client('s3')
    bucket_name = project_name + "-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    return bucket_name
