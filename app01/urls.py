from django.contrib import admin
# from django.urls import path,re_path
# from app01 import views
#
# urlpatterns = [
#     path('index/',views.index),
# ]





from django.contrib import admin
from django.urls import path,re_path,include
from app01 import views
from urldy import yi

app_name = 'app01'
urlpatterns = [
    re_path('user_edit-(\d+)/', views.user_edit),
    re_path('user_del-(\d+)/', views.user_del),
    path('yi/', yi.yi),
    path('login/', views.login),
    path('home/', views.home,name='h1'),
    path('upload/', views.Upload.as_view()),
    path('user_info/', views.user_info),
    path('test_ajax/', views.test_ajax),
    path('diqu/', views.diqu),
    path('t1/', views.t1),
    path('t2/', views.t2),
    path('page/', views.page),
    path('form/', views.form),

]