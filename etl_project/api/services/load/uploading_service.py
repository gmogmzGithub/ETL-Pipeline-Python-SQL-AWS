import boto3
from botocore.exceptions import NoCredentialsError

class UploadService:
    @staticmethod
    def upload_to_s3(file_path, bucket_name, s3_file_name):
        # Initialize the S3 client
        s3 = boto3.client('s3')

        try:
            # Upload the file to the specified S3 bucket
            s3.upload_file(file_path, bucket_name, s3_file_name)
            print(f"Upload Successful: {s3_file_name}")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
