import os
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers.serializers import DataInputSerializer
from .services.extraction.text_extraction_service import ExtractionService
from .services.transform.transformation_service import TransformationService
from .services.load.s3_upload_service import S3UploadService
from .services.load.mongo_service import MongoService
from .services.extraction.mysql_inserter import MySQLInserter
from .services.extraction.models.favorite_tweets import FavoriteTweet
from .services.load.postgres_inserter import PostgresInserter
from .utils import convert_object_id_to_str

@api_view(['GET'])
def extract_data(request):
    # Extract the data from the CoffeeChain.txt file
    file_path = os.path.join(settings.BASE_DIR, 'resources', 'datasets', 'CoffeeChain.txt')
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
    upload_success = S3UploadService.upload_to_s3(csv_file_path, s3_bucket_name, s3_file_name)

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
    

@api_view(['POST'])
def test_mysql(request):
    # TODO -  I will need this to be called later with a Lambda AWS
    mysql_host = settings.MYSQL['HOST']
    mysql_user = settings.MYSQL['USER']
    mysql_password = settings.MYSQL['PASSWORD']
    mysql_database = settings.MYSQL['DATABASE']

    file_path = os.path.join(settings.BASE_DIR, 'resources', 'datasets', 'favorite-tweets.jsonl')

    inserter = MySQLInserter(mysql_host, mysql_user, mysql_password, mysql_database)
    inserter.parse_jsonl_and_insert(file_path)

    # Return a response indicating success
    return Response({"message": "Data inserted into MySQL successfully"})

@api_view(['POST'])
def mirror_data_to_postgres(request):
    # MySQL and PostgreSQL connection details
    mysql_host = settings.MYSQL['HOST']
    mysql_user = settings.MYSQL['USER']
    mysql_password = settings.MYSQL['PASSWORD']
    mysql_database = settings.MYSQL['DATABASE']

    postgres_host = settings.POSTGRES['HOST']
    postgres_user = settings.POSTGRES['USER']
    postgres_password = settings.POSTGRES['PASSWORD']
    postgres_database = settings.POSTGRES['DATABASE']

    # Create MySQLInserter and PostgresInserter instances
    mysql_inserter = MySQLInserter(mysql_host, mysql_user, mysql_password, mysql_database)
    postgres_inserter = PostgresInserter(postgres_host, postgres_user, postgres_password, postgres_database)

    # Get the latest timestamp from PostgreSQL
    latest_timestamp = postgres_inserter.get_latest_timestamp()

    # Fetch records from MySQL that are newer than the latest timestamp
    query = "SELECT * FROM favorite_tweets WHERE CreatedAt > %s"
    mysql_inserter.cursor.execute(query, (latest_timestamp,))
    new_tweets = mysql_inserter.cursor.fetchall()

    # Insert new tweets into PostgreSQL
    for tweet in new_tweets:
        tweet_data = {
            'Text': tweet[1],  # Assuming column index 1 is 'Text'
            'UserName': tweet[2],  # Column index for 'UserName'
            'LinkToTweet': tweet[3],
            'FirstLinkUrl': tweet[4],
            'CreatedAt': tweet[5],
            'TweetEmbedCode': tweet[6],
        }
        postgres_inserter.insert_tweet(tweet_data)

    # Close the connections
    mysql_inserter.close()
    postgres_inserter.close()

    return Response({"message": "Data mirrored from MySQL to PostgreSQL successfully"})