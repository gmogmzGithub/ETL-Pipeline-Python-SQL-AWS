import os
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers.serializers import DataInputSerializer
from .services.extraction.text_extraction_service import ExtractionService
from .services.transform.transformation_service import TransformationService
from .services.load.uploading_service import UploadService
from .services.load.mongo_service import MongoService
from .utils.utils import convert_object_id_to_str

@api_view(['GET'])
def extract_data(request):
    # Extract the data from the CoffeeChain.txt file
    file_path = os.path.join(settings.BASE_DIR, 'resources', 'CoffeeChain.txt')
    data = ExtractionService.extract_from_file(file_path)
    
    # Transform the extracted data
    transformed_data = TransformationService.transform_data(data)
    
    # Save the transformed data to MongoDB and get inserted IDs
    mongo_inserted_ids = MongoService.insert_transformed_data(transformed_data)

    # Convert ObjectIds to string in transformed data and mongo_inserted_ids
    transformed_data = convert_object_id_to_str(transformed_data)
    mongo_inserted_ids = convert_object_id_to_str(mongo_inserted_ids)

    # Save the transformed data to a CSV file
    csv_file_path = TransformationService.save_to_csv(transformed_data)

    # Upload the CSV file to AWS S3
    s3_bucket_name = 'etl-pipeline-python-sql-aws'  # Your S3 bucket name
    s3_file_name = 'transformed_data.csv'  # File name in S3
    upload_success = UploadService.upload_to_s3(csv_file_path, s3_bucket_name, s3_file_name)

    # Return the transformed data, MongoDB inserted IDs, and upload status
    return Response({
        'message': 'Data transformed, saved to MongoDB, and uploaded to S3',
        'mongo_inserted_ids': mongo_inserted_ids,
        'csv_file_path': csv_file_path,
        'transformed_data': transformed_data
    })


@api_view(['POST'])
def transform_data(request):
    serializer = DataInputSerializer(data=request.data)
    if serializer.is_valid():
        # If data is valid, perform the transformation logic
        name = serializer.validated_data['name']
        age = serializer.validated_data['age']
        transformed_data = {'name_uppercase': name.upper(), 'age_next_year': age + 1}
        return Response({'transformed_data': transformed_data})
    else:
        # Return validation errors
        return Response(serializer.errors, status=400)