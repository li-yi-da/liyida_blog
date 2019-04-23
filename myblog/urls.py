from django.urls import path,re_path,include
from myblog import views
urlpatterns = [
    path('index/', views.index),
    path('test/', views.test),
    path('classify/', views.classify),
    path('admin/', views.admin),
    path('create/', views.create),
    path('delete/', views.delete),
    path('login/', views.login),
    path('login_ajax/', views.login_ajax),
    path('logout/', views.logout),
    re_path('label-(\d+)/', views.label),
    re_path('label_admin-(\d+)/', views.label_admin),
    re_path('classify-(\d+)/', views.classify),
    re_path('classify_admin-(\d+)/', views.classify_admin),
    re_path('detail-(\d+)/', views.detail),
    re_path('edit-(\d+)/', views.edit),             #通过正则接受并传递数据  views函数内要设置参数接受
]
