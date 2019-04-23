from django.db import models

# Create your models here.
# class UserType(models.Model):
#     usertype = models.CharField(max_length=64,)




class UserType(models.Model):
    usertype = models.CharField(max_length=64,)
    b = models.ManyToManyField('UserInfo')

class Userdiqu(models.Model):
    userdiqu = models.CharField(max_length=64)
    b = models.ManyToManyField('UserInfo')

class UserInfo(models.Model):

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    usertp = models.ForeignKey('UserType',to_field='id',on_delete=models.CASCADE,)

class UserTest(models.Model):

    name = models.CharField(max_length=32)
    aaa = models.ForeignKey('UserInfo',to_field='id',on_delete=models.CASCADE,)


