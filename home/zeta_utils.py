from django.utils.datastructures import MultiValueDictKeyError
from .constants import base_url, ifid, headers, bundleId, ifid, fundingAccountId
import requests, json
from datetime import date, datetime
import hashlib


def issue_bundle(user):
    url = f'{base_url}/ifi/140793/bundles/{bundleId}/issueBundle'
    data = {
        "accountHolderID": user.AccountHolderId,
        "name": "kawach4 wallet bundle",
        "phoneNumber": '+91' + user.phone
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    print(response.json())
    return None


def create_account_holder(request):
    '''
    Pass the request object of form, use inst later
    '''
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

    url = 'https://fusion.preprod.zeta.in/api/v1/ifi/140793/applications/newIndividual'

    data = {
        "ifiID":
        ifid,
        # "formID": "user.random_slug",
        "spoolID":
        "123",
        "individualType":
        "REAL",
        "salutation":
        Salutation,
        "firstName":
        FirstName,
        "middleName":
        MiddleName,
        "lastName":
        LastName,
        "profilePicURL":
        ProfilePic,
        "dob": {
            "year": Dob.split('-')[0],
            "month": Dob.split('-')[1],
            "day": Dob.split('-')[2]
        },
        "gender":
        Gender,
        "mothersMaidenName":
        MothersMaidenName,
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
            "value": '+91' + Phone,
            "isVerified": "false"
        }, {
            "type": "e",
            "value": Email,
            "isVerified": "false"
        }],
    }

    # print(data, headers)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    print(response.json())
    return False


def fetch_account_details_from_mail(mail):
    url = f'{base_url}/ifi/{ifid}/individualByVector/e/{mail}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        return None


def get_account_transactions(account_id, page_size, page_number):
    url = f'{base_url}/ifi/{ifid}/accounts/{account_id}/transactions?pageSize={page_size}&pageNumber={page_number}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    print(response.json())
    return None


def make_transaction(credit_account_id, debit_account_id, amount):
    h = hashlib.sha3_512()  # Python 3.6+
    h.update(
        bytes(
            credit_account_id + str(datetime.now()) + debit_account_id +
            str(amount), 'utf-8'))
    request_id = h.hexdigest()
    url = f'{base_url}/ifi/{ifid}/transfers'
    data = {
        "requestID": request_id,
        "amount": {
            "currency": "INR",
            "amount": amount
        },
        "transferCode": "ATLAS_P2M_AUTH",
        "creditAccountID": credit_account_id,
        "debitAccountID": debit_account_id,
        "transferTime": 5000,
        "remarks": "Fund Account Holders account",
        "attributes": {}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    print(response.json())
    return None
