from django.urls import path
from .views import update_company, company_details

urlpatterns =[
    path('update-company/', update_company, name='update-company'),
    path('company-details/<int:pk>/', company_details, name='company-details')
]