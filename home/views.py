from django.contrib.auth import logout as auth_logout, login as auth_login
from django.http.request import validate_host
from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.functional import LazyObject
from .models import UserDetail, SavedAccount

import requests, json
from .constants import base_url, ifid, headers, bundleId, ifid, fundingAccountId
from .zeta_utils import create_account_holder, issue_bundle, fetch_account_details_from_mail

# Create your views here.


def home(request):
    return render(request, 'login.html')


# def login(request):
#     return render(request,'login.html')


def dashboard(request):
    # details=UserDetail.objects.filter(user=request.user)
    # print(request.user)
    context = {'username': request.user}
    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contactUs.html')


def underprogress(request):
    return render(request, 'underprogress.html')


def login(request):
    if request.method == 'POST':
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('dashboard')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'successfully logged out')
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
            Password = request.POST['password']
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

            inst = UserDetail(user=user,
                              AccountHolderId=res['individualID'],
                              salutation=Salutation,
                              firstName=FirstName,
                              middleName=MiddleName,
                              lastName=LastName,
                              Gender=Gender,
                              Aadhar=Aadhar,
                              phone=Phone,
                              Email=Email)

            issue_bundle_res = issue_bundle(inst)
            if issue_bundle_res:
                inst.AccountId = issue_bundle_res['accounts'][0]['accountID']
            else:
                messages.error(
                    request,
                    "Can not create account, Kindly reach out to us on customer services."
                )
                return redirect('login')

            inst.save()

            messages.success(request, "Account Added Successfully")
            # return render(request,'index.html')
            return redirect('login')
        except ValueError:
            messages.error(
                request,
                "Can not create account, Kindly reach out to us on customer services."
            )
            return redirect('home')

    return render(request, 'createacc.html')


def accounts(request):
    if request.method == 'POST':
        try:
            name = request.POST['accholder']
            username = request.POST['accno']
            usr = request.user
            res = fetch_account_details_from_mail(username)
            if not res:
                messages.error(
                    request,
                    "Some error occoured, kindly contact customer service")
                return redirect('accounts')

            inst = SavedAccount(user=usr,
                                accHolderName=f"{res['firstName']} {res['lastName']}",
                                accUserName=username)
            inst.save()
            messages.success(request, "Account Added Successfully!")
            return redirect('accounts')
        except ValueError:
            messages.error(
                request,
                "Some error occoured, kindly contact customer service")
            return redirect('accounts')

    accs = SavedAccount.objects.filter(user=request.user)
    context = {'accs': accs}
    return render(request, 'accounts.html', context)
