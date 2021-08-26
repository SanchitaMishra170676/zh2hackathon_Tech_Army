from django.shortcuts import render, redirect 
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'login.html') 
  
def login(request):    
    return render(request,'login.html')

def dashboard(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contactUs.html')

def underprogress(request):
    return render(request,'underprogress.html')

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
            messages.success(request,"Account Added Successfully")
            # return render(request,'index.html')
            return redirect('dashboard')
        except:
            messages.error(request,"Can not create account, Kindly reach out to us on customer services.")
            return redirect('home')

    return render(request,'createacc.html')