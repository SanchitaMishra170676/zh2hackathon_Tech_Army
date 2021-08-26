from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# Create your models here.

""" User Model """
class UserDetail(models.Model):
    user= models.OneToOneField(to=User,default= None, on_delete= models.CASCADE)
    AccountHolderId= models.CharField(max_length=50)
    AccountId = models.CharField(max_length=50,null=True)
    salutation= models.CharField(max_length=5)
    firstName= models.CharField(max_length=100)
    middleName=models.CharField(max_length=100, null=True)
    lastName= models.CharField(max_length=100)
    Gender= models.CharField(max_length=10)
    Aadhar = models.CharField(max_length=20)
    Email = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.firstName +" " +self.lastName

class SavedAccount(models.Model):
    user= ForeignKey(to=User,default= None, on_delete= models.CASCADE)
    accHolderName = models.CharField(max_length=50)
    accUserName=models.CharField(max_length=50)

    def __str__(self):
        return self.accHolderName


