from django.urls import path
from . import views

urlpatterns = [
    path('extract', views.extract_data, name='extract_data'),
    path('transform', views.transform_data, name='transform_data'),
]