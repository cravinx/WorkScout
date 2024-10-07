from django.urls import path
from .views import register_applicant, register_recruiter, login_user, logout_user

urlpatterns = [
    path('register-applicant/', register_applicant, name='register-applicant'),
    path('register-recruiter/', register_recruiter, name='register-recruiter'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]