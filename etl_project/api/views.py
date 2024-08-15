from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def extract_data(request):
    # This will be the entry point for extracting data
    data = {'message': 'Data extraction initiated'}
    return Response(data)