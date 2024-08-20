from django.urls import path
from . import views

urlpatterns = [
    path('extract', views.extract_data, name='extract_data'),
    path('transform', views.transform_data, name='transform_data'),
    path('testmysql', views.test_mysql, name='test_mysql'),
    path('mirrordata', views.mirror_data_to_postgres, name='mirror_mysql'),
]