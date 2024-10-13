from django.urls import path
from .views import update_resume, resume_details

urlpatterns =[
    path('update-resume/', update_resume, name='update-resume'),
    path('resume-details/', resume_details, name='resume-details'),
]