from django.urls import path
from .views import home, job_listing, job_details


urlpatterns = [
    path('', home, name='home'),
    path('job-listing/', job_listing, name='job-listing'),
    path('job-details/<int:pk>/', job_details, name='job-details'),
]