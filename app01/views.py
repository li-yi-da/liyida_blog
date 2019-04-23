#
# from django.shortcuts import render,HttpResponse,redirect
# # Create your views here.
#
#



from django.shortcuts import render,HttpResponse,redirect
import os
from app01 import models
from django.urls import reverse



def login(request):
    error_msg = ''
    if request.method == 'POST':
        user = request.POST.get('user',None)
        psw  = request.POST.get('psw',None)
        obj = models.UserInfo.objects.filter(username=user,password=psw).first()
        r = redirect('/app01/user_info/')
        if obj:
            r.set_cookie('username',user)
            request.session['username']= user
            request.session['login_m']= True
            # request.session.set_expiry(0)
            return r

        else:
            error_msg = '密码错误'
        # print(request.method)
    return render(request,'login.html',{'error_msg':error_msg})



def user_info(request):
    if request.method == 'GET':
        # cook = request.COOKIES.get('username')
        # if cook:
        if request.session.get('login_m', None):
            re = request.session['username']
            print(re)
            obj = models.UserInfo.objects.all()
            obj2 = models.UserType.objects.all()
            return render(request, 'user_info.html', {'obj_list': obj, 'obj_list2': obj2,'re':re})
        else:
            return redirect('/app01/login/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tp = request.POST.get('type')
        models.UserInfo.objects.create(username=username,password=password,usertp_id=tp)
        return redirect('/app01/user_info/')



def user_edit(request,nid):
    if request.method == 'GET':
        obj = models.UserInfo.objects.filter(id=nid).first()
        return render(request,'user_edit.html',{'obj_list':obj})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        models.UserInfo.objects.filter(id=nid).update(username=username,password=password)
        return redirect('/app01/user_info/')



def user_del(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/app01/user_info/')



def test_ajax(request):
    import json
    dat = {'alt':True,'errormes':None,'data':None,}
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            tp = request.POST.get('type')
            if username and len(username)<=8:
                models.UserInfo.objects.create(username=username,password=password,usertp_id=tp)
            else:
                dat['alt'] = False
                dat['errormes'] = '不符合规范'
        except Exception as e:
            dat['alt'] = False
            dat['errormes'] = '服务器错误'

        return HttpResponse(json.dumps(dat))



user_list=[
    {'user':'liyida','email':'162','gender':'男'},
    {'user':'zhans','email':'1eqw2','gender':'男'},
    {'user':'xiewe','email':'16qwe','gender':'男'}
]
# 外键values操作
def home(request):
    # for i in range(20):
    #     temp = {'user': 'liyida'+str(i), 'email': '162', 'gander': '男'}
    #     user_list.append(temp)
    print(reverse('a1:h1')) #命名空间
    obj = models.UserTest.objects.values('name','aaa__username','aaa__password','aaa_id')
    for i in obj:
        print(i['name'],i['aaa__username'],i['aaa__password'],i['aaa_id'],)

    # print(obj)
    if request.method == 'POST':
        u = request.POST.get('username',None)
        e = request.POST.get('email',None)
        g = request.POST.get('gender',None)
        temp = {'user':u,'email':e,'gender':g}
        user_list.append(temp)
    return render(request,'home.html',{'user_list':user_list})



def diqu(request):
    diqu_list = models.Userdiqu.objects.all()
    for i in diqu_list:
        print(i.b.all())
    return render(request,'diqu.html',{'diqu_list':diqu_list})



# 下面为 get和post的类写法
from django.views import View
# ------------------------------------------------------------------------------
class Upload(View):
    def dispatch(self, request, *args, **kwargs):
        print('liyida')
        result =  super(Upload,self).dispatch(request,*args,**kwargs)
        return result

    def get(self,request):
        return render(request, 'upload.html')

    def post(self,request):
        r = request.POST.getlist('c', None)
        print(r)
        b = request.FILES.get('f', None)
        if b :
            print(b,type(b),b.chunks(),len(b))
            file_path = os.path.join('uploads',b.name)
            fi = open(file_path, mode='wb')
            for i in b.chunks():
                fi.write(i)
            fi.close()
        return render(request, 'upload.html')



def t1(request):
    return render(request,'t1.html')



def t2(request):
    return render(request,'t2.html')



page_list=[]

for i in range(1,209):
    page_list.append(i)

from django.utils.safestring import mark_safe

def page(request):
    p = request.GET.get('p',1)   # 1是默认值
    p = int(p)
    page_fen=page_list[(p-1)*10:p*10]
    c_p = len(page_list)
    c, y = divmod(c_p,10)   #c_p除以10，把商和余数已元祖返回
    if y:
        c +=1
    p_b=[]
    for i in range(1,c+1):
        item = '<a href="/cmdb/page/?p=%s">%s</a>' %(i,i)
        item = mark_safe(item)    #把item变成被前端承认的合法字符
        p_b.append(item)
    return render(request,'page.html',{'page_fen':page_fen,'p_b':p_b})



from django import forms
from django.forms import widgets
from django.forms import fields
class Form(forms.Form):
    user = fields.CharField(
        error_messages={'required':'用户名不能为空'},
    )
    password = fields.CharField(
        max_length= 12,
        min_length= 6,
        error_messages={'required':'密码不能为空','max_length':'长了','min_length':'短了'},
    )
    email = fields.EmailField(
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
    )
    # test = fields.EmailField()

#下方需要上方的类，但不属于上方的类，不要缩进
def form(request):
    if request.method == 'GET':
        obj = Form()
        return render(request,'form.html',{'obj':obj})

    if request.method == 'POST':
        obj = Form(request.POST)
        print(obj)
        r1 = obj.is_valid()
        print(r1)
        if r1:
            print('ok')
        else:
            # print(obj.errors.as_json())
            # print(obj.errors['user'][0])
            return render(request,'form.html',{'obj':obj})

        return redirect('/app01/form/')