from django.urls import path
from .views import create_job, update_job,manage_jobs, apply_to_job, all_applicants, applied_jobs, response, apply_email

urlpatterns = [
    path('create-job/', create_job, name='create-job'),
    path('update-job/<int:pk>/', update_job, name='update-job'),
    path('manage-jobs/', manage_jobs, name='manage-jobs'),
    path('apply-to-job/<int:pk>', apply_to_job, name='apply-to-job'),
    path('all-applicants/<int:pk>/', all_applicants, name='all-applicants'),
    path('applied-jobs/', applied_jobs, name='applied-jobs'),
    path('all-applicants/<int:pk>/response', response, name='response'),
    # path('all-applicants/<int:pk>/respond-email', respond_email, name='respond-email'),
    path('apply-to-job/apply-email/<int:pk>', apply_email, name='apply-email'),

]