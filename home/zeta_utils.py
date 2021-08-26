def issue_bundle(user):
    url = 'https://fusion.preprod.zeta.in/api/v1/ifi/140793/applications/newIndividual'
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
    return False

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
    print(Dob.split('-'), response.json())
    return False
