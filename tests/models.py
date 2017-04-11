from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Categories(models.Model):

    cname = models.CharField(max_length=30)

    def __unicode__(self):
        return self.cname



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    passcheck = models.CharField(max_length= 30,default= 0)
    contact = models.CharField(max_length=30)

    def __unicode__(self):
         return '%s' % (self.user)

class Softwares(models.Model):
    name = models.CharField(max_length = 50)
    productimage = models.ImageField(upload_to = 'media/softwares/productimages')
    link = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    seller = models.CharField(max_length = 50)
    list = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    companylogo = models.ImageField(upload_to='nedia/companylogos')

    def __unicode__(self):
        return self.name

class Purchases(models.Model):
    curruser = models.ForeignKey(UserProfile)
    softwareinfo = models.ForeignKey(Softwares)
    categoryinfo = models.ForeignKey(Categories)
    macid1 = models.CharField(default=0, max_length=50)
    macid2 = models.CharField(default=0, max_length=50)
    macid3 = models.CharField(default=0, max_length=50)
    maccount = models.IntegerField(default=0)
    purchasetime = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.curruser.user.first_name