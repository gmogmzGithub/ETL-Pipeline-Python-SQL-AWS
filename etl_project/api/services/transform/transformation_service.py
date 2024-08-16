import boto3
import csv
import os
from django.conf import settings
from botocore.exceptions import NoCredentialsError

class TransformationService:
    @staticmethod
    def transform_data(data):
        transformed_data = []
        for record in data:
            # Example transformation: convert 'Product' field to uppercase
            record['Product'] = record['Product'].upper()

            # Example transformation: calculate the profit margin (Profit/Sales)
            try:
                record['Profit Margin'] = round(float(record['Profit']) / float(record['Sales']) * 100, 2)
            except (ValueError, ZeroDivisionError):
                record['Profit Margin'] = None

            # Append the transformed record
            transformed_data.append(record)

        return transformed_data

    @staticmethod
    def save_to_csv(data, file_name="transformed_data.csv"):
        # Define the path where the CSV will be saved
        file_path = os.path.join(settings.BASE_DIR, 'resources', file_name)

        # Get the fieldnames from the first dictionary
        fieldnames = data[0].keys()

        # Write the data to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data rows
            for row in data:
                writer.writerow(row)

        return file_path

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
