from django.db import models

# Create your models here.
#创建文章表
class Article(models.Model):
    title = models.CharField(max_length=32)
    introduce = models.CharField(max_length=64)
    content = models.TextField()
    addtime = models.DateField(auto_now_add=True)
    updatatime = models.DateField(auto_now=True)
    classify = models.ForeignKey('Classify',to_field='id',on_delete=models.CASCADE,)
    label = models.ManyToManyField('Label')
    liulangliang = models.IntegerField(default=0)

#创建分类表
class Classify(models.Model):
    classify = models.CharField(max_length=32)


#创建标签表
class Label(models.Model):
    label = models.CharField(max_length=32)


#用户
class User(models.Model):
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

#评论
class Pinglun(models.Model):
    name = models.CharField(max_length=16)
    cont = models.CharField(max_length=128)
    addtime = models.DateTimeField(auto_now_add=True)
    arti = models.ForeignKey('Article',to_field='id',on_delete=models.CASCADE,)