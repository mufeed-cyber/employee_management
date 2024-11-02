from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list_create, name='employee_list_create'),
    path('employees/<int:id>/', views.employee_detail, name='employee_detail'),
]
