from django.contrib.auth import logout as auth_logout, login as auth_login
from django.http.request import validate_host
from django.shortcuts import render, redirect,HttpResponse,Http404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.functional import LazyObject
from django.utils.datastructures import MultiValueDictKeyError
from .models import UserDetail

import requests, json

# Create your views here.

def home(request):
    return render(request,'login.html') 
# def login(request):    
#     return render(request,'login.html')

def dashboard(request):
    # details=UserDetail.objects.filter(user=request.user)
    # print(request.user)
    context={'username':request.user}
    return render(request,'index.html',context)

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
            Email = request.POST['email']
            Password= request.POST['password']
            Gender = request.POST['gender']
            Aadhar = request.POST['aadhar']
            Email = request.POST['email']
            Phone = request.POST['phone']

            res = create_account_holder(request)
            if res:
                messages.success(request, "Account Added Successfully")
            else:
                messages.error(
                    request,
                    "Can not create account, Kindly reach out to us on customer services."
                )
                return redirect('login')
            
            user = User.objects.create_user(username=Email, password=Password)
            user.first_name = FirstName
            user.last_name = LastName
            
            inst=UserDetail(user=user,AccountHolderId=res['individualID'],salutation= Salutation, firstName=FirstName, middleName= MiddleName,lastName=LastName,Gender=Gender, Aadhar=Aadhar,phone=Phone)
            inst.save()
            # user.form_id = 
            
            messages.success(request,"Account Added Successfully")
            # return render(request,'index.html')
            return redirect('login')
        except ValueError:
            messages.error(request,"Can not create account, Kindly reach out to us on customer services.")
            return redirect('home')

    return render(request,'createacc.html')

def create_account_holder(request):
    Salutation = request.POST['salutation']
    FirstName = request.POST['first-name']
    MiddleName = request.POST['middle-name']
    LastName = request.POST['last-name']
    Gender = request.POST['gender']
    MothersMaidenName = request.POST['mmn']
    Aadhar = request.POST['aadhar']
    Email = request.POST['email']
    Phone = request.POST['phone']
    try:
        Dob = request.POST['dob']
    except ValueError:
        Dob = "28-09-2001"
    try:
        ProfilePic = request.FILES['profilepic']
    except MultiValueDictKeyError:
        # using a random image for now
        ProfilePic = 'https://cdn2.iconfinder.com/data/icons/avatars-99/62/avatar-370-456322-512.png'

    from .constants import base_url, zeta_auth_token, ifid
    url = 'https://fusion.preprod.zeta.in/api/v1/ifi/140793/applications/newIndividual'
    
    data = {
        "ifiID": ifid,
        # "formID": "user.random_slug",
        "spoolID": "123",
        "individualType": "REAL",
        "salutation": Salutation,
        "firstName": FirstName,
        "middleName": MiddleName,
        "lastName": LastName,
        "profilePicURL": ProfilePic,
        "dob": {
            "year": Dob.split('-')[0],
            "month": Dob.split('-')[1],
            "day": Dob.split('-')[2]
        },
        "gender": Gender,
        "mothersMaidenName": MothersMaidenName,
        "kycDetails": {
            "kycStatus": "MINIMAL",
            "kycStatusPostExpiry": "string",
            "kycAttributes": {},
            "authData": {
                "PAN": Aadhar
            },
            "authType": "PAN"
        },
        "vectors": [{
            "type": "p",
            "value": Phone,
            "isVerified": "false"
        }, 
        {
            "type": "e",
            "value": Email,
            "isVerified": "false"
        }],
    }
    headers = {
        "Content-type": "application/json",
        "X-Zeta-AuthToken": zeta_auth_token
    }

    
    # print(data, headers)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    return False



def accounts(request):
    return render(request,'accounts.html')