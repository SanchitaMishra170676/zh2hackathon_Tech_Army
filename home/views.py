from django.shortcuts import render, redirect 
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'login.html') 
  
def login(request):    
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def dashboard(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contactUs.html')

def underprogress(request):
    return render(request,'underprogress.html')