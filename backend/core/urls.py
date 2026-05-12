from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('hospital/<int:hospital_id>/', views.hospital_detail),
    path('add_review/', views.add_review),
    path('api/hospitals/', views.hospitals_list, name='hospitals_list'),
    path('api/compare/', views.compare_hospitals, name='compare_hospitals'),
    path('api/doctors/', views.doctors_list, name='doctors_list'),
    path('api/doctor/<int:doctor_id>/', views.doctor_detail_api, name='doctor_detail_api'),
    path('api/register/', views.register, name='register'),
    path('api/book_appointment/', views.book_appointment, name='book_appointment'),
    path('api/appointments/', views.appointments_list, name='appointments_list'),
    path('api/add_hospital/', views.add_hospital, name='add_hospital'),
    path('api/add_doctor/', views.add_doctor, name='add_doctor'),
    path('api/delete_hospital/', views.delete_hospital, name='delete_hospital'),
    path('api/delete_doctor/', views.delete_doctor, name='delete_doctor'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]