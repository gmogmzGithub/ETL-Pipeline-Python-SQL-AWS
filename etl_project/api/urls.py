from django.contrib import admin
from django.urls import path, include  # Make sure to include 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Add this to include the api app's URLs
]