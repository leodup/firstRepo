import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import boto3

try:
    # Download file from S3
    file_name = input('\n*************************************\nFile name: ')

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',#
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    # Download file and read from disc
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket='test-bucket-disregard', Key=file_name)
    data = response['Body'].read()
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    
    # Create the container
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "s3-container"
    
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    print("\nUploading to Azure Storage as blob")

    #Upload the created file
    blob_client.upload_blob(data)
    print('\nUpload successful\n')

    # Delete file
    print('Deleting...\t', end = '')
    s3.Object('test-bucket-disregard', file_name).delete() # From S3
    os.remove("./temp.csv") # From local

    print('S3 File deleted\n*************************************\n')

except Exception as ex:
    print('Exception:')
    print(ex)