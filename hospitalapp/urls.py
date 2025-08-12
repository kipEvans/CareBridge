
from django.contrib import admin
from django.urls import path

from hospitalapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.index, name='index'),
    path('service/', views.service, name='service-details'),
    path('starter/', views.starter, name='starter-page'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contacts, name='contacts'),
    path('appointment/', views.Appointment, name='appointment'),
    path('contact/', views.Contact, name='contact'),
    path('show/', views.show, name='show'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('', views.register, name='register'),
    path('login/', views.loginview, name='login'),

    #Mpesa API URLS
    path('pay/', views.pay, name='pay'),


    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),
]
