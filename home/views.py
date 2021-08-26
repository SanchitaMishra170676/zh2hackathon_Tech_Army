from django.contrib.auth import logout as auth_logout, login as auth_login
from django.shortcuts import render, redirect,HttpResponse,Http404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.functional import LazyObject


# Create your views here.

def home(request):
    return render(request,'login.html') 
  
# def login(request):    
#     return render(request,'login.html')

def dashboard(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contactUs.html')

def underprogress(request):
    return render(request,'underprogress.html')

def login(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpassword=request.POST['password']

        user = authenticate(username =loginusername,password =loginpassword)

        if user is not None:
            auth_login(request,user)
            messages.success(request,'Logged in Successfully')
            return redirect ('dashboard')
        
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')

    return render(request,'login.html')


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,'successfully logged out')
        return redirect('home')
    else:
        return HttpResponse('404 Not found')


def createaccount(request):
    if request.method == "POST":
        try:
            Salutation = request.POST['salutation']
            FirstName = request.POST['first-name']
            MiddleName = request.POST['middle-name']
            LastName = request.POST['last-name']
            Gender = request.POST['gender']
            MothersMaidenName = request.POST['mmn']
            Aadhar = request.POST['aadhar']
            Email = request.POST['email']
            Phone = request.POST['phone']
            Password= request.POST['password']
            try:
                Dob = request.POST['dob']
            except:
                Dob= "28-09-2001"
            try:
                ProfilePic=  request.FILES['profilepic']
            except:
                pass      

            user = User.objects.create_user(username=Email, password=Password)
            user.first_name = FirstName
            user.last_name = LastName
            # user.form_id = 
            messages.success(request,"Account Added Successfully")
            # return render(request,'index.html')
            return redirect('login')
        except:
            messages.error(request,"Can not create account, Kindly reach out to us on customer services.")
            return redirect('home')

    return render(request,'createacc.html')