from datetime import datetime
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.http.request import validate_host
from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.functional import LazyObject
from .models import UserDetail, SavedAccount
from django.core.mail import send_mail, EmailMessage
from django.core import mail as m

import requests, json
from .constants import base_url, ifid, headers, bundleId, ifid, fundingAccountId
from .zeta_utils import create_account_holder, get_account_transactions, issue_bundle, fetch_account_details_from_mail, make_transaction

# Create your views here.


def home(request):
    return render(request, 'login.html')


# def login(request):
#     return render(request,'login.html')


def dashboard(request):
    if request.method == 'POST':
        try:
            Accholder = request.POST['accHolderName']
            Amount = int(request.POST['amt'])
            print(Accholder, Amount)
            # TODO: Get the limit from Database
            if Amount > 5:
                connection = m.get_connection()
                Em = "sanchitamishra170676@gmail.com"
                connection.open()
                message = render_to_string('email.html', {})
                email_ver = EmailMessage("Kawach Confirmation",
                                         message,
                                         to=[Em])
                email_ver.content_subtype = 'html'
                email_ver.send()
                connection.close()
                messages.warning(request,
                                 "Transaction pending till trustee aprroves")
            else:
                mail = Accholder.split('-')[1]
                credit_accountID = UserDetail.objects.get(Email=mail).AccountId
                debit_accountID = UserDetail.objects.get(
                    user=request.user).AccountId
                print(mail, credit_accountID, debit_accountID)
                if make_transaction(credit_accountID, debit_accountID, Amount):
                    messages.success(request, "Transaction Successful")
                else:
                    messages.error(request, "Transaction Failed")
                    return redirect('dashboard')
        except ValueError as v:
            print(v)
            messages.error(request, "Transaction Failed")
            return redirect('dashboard')
    accs = SavedAccount.objects.filter(user=request.user)
    context = {'username': request.user, 'accs': accs}
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
            # Put some default money
            transaction_res = make_transaction(inst.AccountId,
                                               fundingAccountId, 100)
            print(transaction_res)
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

            inst = SavedAccount(
                user=usr,
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


def passbook(request):
    userObj = UserDetail.objects.get(Email=request.user)
    accountID = userObj.AccountId
    res = get_account_transactions(accountID, 20, 1)
    for transaction in res['accountTransactionList']:
        transaction['email'] = str(request.user)
        transaction['name'] = userObj.firstName + ' ' + userObj.lastName
        transaction['timestamp'] = str(
            datetime.fromtimestamp(int(str(transaction['timestamp'])[0:10])))
        transaction['date'] = transaction['timestamp'].split(' ')[0]
        transaction['time'] = transaction['timestamp'].split(' ')[1]
    print(res)
    return render(request, 'passbook.html', {'transactions': res})
