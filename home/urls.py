from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('contact-us/', views.contact, name='contact'),
    path('underprogress/', views.underprogress, name='underprogress'),
    path('sign-up/', views.createaccount, name='createacc'),
]