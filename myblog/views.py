from django.shortcuts import render,HttpResponse,redirect
from myblog import models
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.



#前台的分页类
class Page():
    def __init__(self, article_list, page_cont, p, d):  #d是url对应的def
        self.article_list = article_list
        self.page_cont = int(page_cont)
        self.p = int(p)
        self.d = d
        c_p = len(self.article_list)
        c, y = divmod(c_p, self.page_cont)  # c_p除以10，把商和余数已元祖返回
        if y:
            c += 1  # c为一共能分成多少页
        self.c = c

    def c_d(self):
        return self.c

    def page_fen_d(self):
        if 1 <= self.p <= self.c:
            page_fen = self.article_list[(self.p - 1) * self.page_cont : self.p * self.page_cont]  # 一页要显示self.page_cont篇文章
        else:
            page_fen = []
        return page_fen

    def p_b_d(self):
        p_b_s = []  # 分页列表
        for i in range(1, self.c + 1):
            if i == self.p:
                item = '<a href="/myblog/%s/?p=%s" style="color: red">第%s页</a>' % (self.d, i, i)
            else:
                item = '<a href="/myblog/%s/?p=%s">第%s页</a>' % (self.d, i, i)
            item = mark_safe(item)  # 把item变成被前端承认的合法字符
            p_b_s.append(item)
        if 1 <= self.p <= self.c:
            if 1 <= self.p <= 5:
                p_b = p_b_s[0:5]
            elif self.c - 5 < self.p <= self.c:
                p_b = p_b_s[self.c - 5:]
            else:
                p_b = p_b_s[self.p - 3:self.p + 2]
        else:
            p_b = []
        return p_b



#分类的分页
class Page_classify():
    def __init__(self, article_list, page_cont, p, nid, d):
        self.article_list = article_list
        self.page_cont = int(page_cont)
        self.p = int(p)
        self.nid = nid
        self.d = d
        c_p = len(self.article_list)
        c, y = divmod(c_p, self.page_cont)  # c_p除以10，把商和余数已元祖返回
        if y:
            c += 1  # c为一共能分成多少页
        self.c = c

    def c_d(self):
        return self.c

    def page_fen_d(self):
        if 1 <= self.p <= self.c:
            page_fen = self.article_list[(self.p - 1) * self.page_cont: self.p * self.page_cont]  # 一页要显示self.page_cont篇文章
        else:
            page_fen = []
        return page_fen

    def p_b_d(self):
        p_b_s = []  # 分页列表
        for i in range(1, self.c + 1):
            if i == self.p:
                item = '<a href="/myblog/%s-%s/?p=%s" style="color: red">第%s页</a>' % (self.d, self.nid, i, i)
            else:
                item = '<a href="/myblog/%s-%s/?p=%s">第%s页</a>' % (self.d, self.nid, i, i)
            item = mark_safe(item)  # 把item变成被前端承认的合法字符
            p_b_s.append(item)
        if 1 <= self.p <= self.c:
            if 1 <= self.p <= 5:
                p_b = p_b_s[0:5]
            elif self.c - 5 < self.p <= self.c:
                p_b = p_b_s[self.c - 5:]
            else:
                p_b = p_b_s[self.p - 3:self.p + 2]
        else:
            p_b = []
        return p_b



#获取文章
from django.utils.safestring import mark_safe
def index(request):
    user_name = ''
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            # user_name = request.COOKIES.get('username')
        classify_m = models.Classify.objects.all()
        article_m = models.Article.objects.all()
        label_m = models.Label.objects.all()
        p = request.GET.get('p', 1)   # 1是默认值
        p = int(p)
        page_m = Page(article_m, 6, p, 'index')
        c = page_m.c_d()
        if len(article_m) == 0:
            page_fen = page_m.page_fen_d()
            p_b = page_m.p_b_d()
            previous_page = p
            next_page = p
        else:
            if 1 <= p <= c:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                if p == 1:
                    if p == c:
                        previous_page = p
                        next_page = p
                    else:
                        previous_page = p
                        next_page = p + 1
                elif p == c:
                    previous_page = p - 1
                    next_page = p
                else:
                    previous_page = p - 1
                    next_page = p + 1

            else:
                return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
        return render(request,'myblog/index.html',{'classify_m':classify_m,
                                                   'label_m':label_m,
                                                   'user_name': user_name,
                                                   'page_fen': page_fen,
                                                   'p_b': p_b,
                                                   'previous_page': previous_page,
                                                   'next_page': next_page,
                                                   'c': c,
                                                   })



def classify(request,nid):
    user_name =''
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
        classify_m = models.Classify.objects.all()
        label_m = models.Label.objects.all()
        classify_now = models.Classify.objects.get(id=nid)
        classify_list = models.Article.objects.filter(classify_id=nid)
        p = request.GET.get('p', 1)  # 1是默认值
        p = int(p)
        page_m = Page_classify(classify_list, 6, p, nid, 'classify')
        c = page_m.c_d()
        if c == 0:
            page_fen = page_m.page_fen_d()
            p_b = page_m.p_b_d()
            previous_page = p
            next_page = p
            classify_list_err = '当前分类无文章'
        else:
            classify_list_err = ''
            if 1 <= p <= c:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                if p == 1:
                    if p == c:
                        previous_page = p
                        next_page = p
                    else:
                        previous_page = p
                        next_page = p + 1
                elif p == c:
                    previous_page = p - 1
                    next_page = p
                else:
                    previous_page = p - 1
                    next_page = p + 1

            else:
                return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
        # 翻页↓
        return render(request,'myblog/classify.html',{'classify_m':classify_m,
                                                      'label_m': label_m,
                                                      'user_name': user_name,
                                                      'page_fen': page_fen,
                                                      'p_b': p_b,
                                                      'previous_page': previous_page,
                                                      'next_page': next_page,
                                                      'c': c,

                                                      'classify_list_err':classify_list_err,
                                                      'classify_now':classify_now,
                                                      })



#标签分类
def label(request,nid):
    # a = models.Article.objects.get(id=2).label.all()
    # print(a)
    # e = models.Label.objects.get(id=4).article_set.all()
    # print(e)
    # a2 = models.Article.objects.filter(id=2).values('title','classify__classify')
    # print(a2)
    # 取出多个id↓
    # b = models.Article.objects.filter(id__in=[2,3])
    # print(b)
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
        else:
            user_name = ''
        label_m = models.Label.objects.all()
        classify_m = models.Classify.objects.all()
        label_list = models.Label.objects.get(id=nid).article_set.all()
        label_now = models.Label.objects.get(id=nid)
        p = request.GET.get('p', 1)  # 1是默认值
        p = int(p)
        page_m = Page_classify(label_list, 6, p, nid, 'label')
        c = page_m.c_d()
        if c == 0:
            page_fen = page_m.page_fen_d()
            p_b = page_m.p_b_d()
            previous_page = p
            next_page = p
            label_list_err = '当前标签无文章'
        else:
            label_list_err = ''
            if 1 <= p <= c:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                if p == 1:
                    if p == c:
                        previous_page = p
                        next_page = p
                    else:
                        previous_page = p
                        next_page = p + 1
                elif p == c:
                    previous_page = p - 1
                    next_page = p
                else:
                    previous_page = p - 1
                    next_page = p + 1

            else:
                return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
        return render(request,'myblog/label.html',{
                                                   'label_m':label_m,
                                                   'classify_m':classify_m,
                                                   'user_name': user_name,
                                                   'page_fen': page_fen,
                                                   'p_b': p_b,
                                                   'previous_page': previous_page,
                                                   'next_page': next_page,
                                                   'c': c,

                                                   'label_list_err':label_list_err,
                                                   'label_now':label_now,
                                                   })



#展示详细文章
def detail(request,nid):
    user_name =''
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
        label_m = models.Label.objects.all()
        classify_m = models.Classify.objects.all()
        article_nid = models.Article.objects.filter(id=nid).first()
        return render(request, 'myblog/detail.html', {'label_m':label_m,
                                                      'classify_m':classify_m,
                                                      'user_name': user_name,
                                                      'article_nid':article_nid,
                                                      })



#管理后台

#后台主页
def admin(request):
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            classify_m = models.Classify.objects.all()
            article_m = models.Article.objects.all()
            label_m = models.Label.objects.all()
            p = request.GET.get('p', 1)  # 1是默认值
            p = int(p)
            page_m = Page(article_m, 10, p, 'admin')
            c = page_m.c_d()
            if c == 0:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                previous_page = p
                next_page = p
            else:
                if 1 <= p <= c:
                    page_fen = page_m.page_fen_d()
                    p_b = page_m.p_b_d()
                    if p == 1:
                        if p == c:
                            previous_page = p
                            next_page = p
                        else:
                            previous_page = p
                            next_page = p + 1
                    elif p == c:
                        previous_page = p - 1
                        next_page = p
                    else:
                        previous_page = p - 1
                        next_page = p + 1

                else:
                    return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
            return render(request,'myblog/admin.html',{'classify_m':classify_m,
                                                       'article_m':article_m,
                                                       'user_name': user_name,
                                                       'label_m':label_m,
                                                       'page_fen': page_fen,
                                                       'p_b': p_b,
                                                       'previous_page': previous_page,
                                                       'next_page': next_page,
                                                       'c': c,
                                                       })
        else:
            return redirect('/myblog/login/')



#后台分类页面
def classify_admin(request,nid):
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            classify_m = models.Classify.objects.all()
            classify_nid = models.Classify.objects.get(id=nid)
            classify_list = models.Article.objects.filter(classify_id=nid)
            label_m = models.Label.objects.all()
            p = request.GET.get('p', 1)  # 1是默认值
            p = int(p)
            page_m = Page_classify(classify_list, 6, p, nid, 'classify_admin')
            c = page_m.c_d()
            if c == 0:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                previous_page = p
                next_page = p
                classify_list_ex = '此分类没有文章'
            else:
                classify_list_ex = ''
                if 1 <= p <= c:
                    page_fen = page_m.page_fen_d()
                    p_b = page_m.p_b_d()
                    if p == 1:
                        if p == c:
                            previous_page = p
                            next_page = p
                        else:
                            previous_page = p
                            next_page = p + 1
                    elif p == c:
                        previous_page = p - 1
                        next_page = p
                    else:
                        previous_page = p - 1
                        next_page = p + 1

                else:
                    return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
            return render(request, 'myblog/classify_admin.html',{'classify_m': classify_m,
                                                                 'label_m': label_m,
                                                                 'classify_list_ex': classify_list_ex,
                                                                 'classify_nid': classify_nid,
                                                                 'user_name': user_name,
                                                                 'page_fen': page_fen,
                                                                 'p_b': p_b,
                                                                 'previous_page': previous_page,
                                                                 'next_page': next_page,
                                                                 'c': c,
                                                                 })
        else:
            return redirect('/myblog/login/')



#后台标签分类
def label_admin(request,nid):
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            classify_m = models.Classify.objects.all()
            label_m = models.Label.objects.all()
            article_label = models.Label.objects.get(id=nid).article_set.all()
            label_now = models.Label.objects.get(id=nid)
            p = request.GET.get('p', 1)  # 1是默认值
            p = int(p)
            page_m = Page_classify(article_label, 6, p, nid, 'label_admin')
            c = page_m.c_d()
            if c == 0:
                page_fen = page_m.page_fen_d()
                p_b = page_m.p_b_d()
                previous_page = p
                next_page = p
                label_list_err = '此标签没有文章'
            else:
                label_list_err = ''
                if 1 <= p <= c:
                    page_fen = page_m.page_fen_d()
                    p_b = page_m.p_b_d()
                    if p == 1:
                        if p == c:
                            previous_page = p
                            next_page = p
                        else:
                            previous_page = p
                            next_page = p + 1
                    elif p == c:
                        previous_page = p - 1
                        next_page = p
                    else:
                        previous_page = p - 1
                        next_page = p + 1

                else:
                    return HttpResponse('<h2 style="margin:100px auto;text-align: center;">输入的页数有误请返回</h2>')
            return render(request, 'myblog/label_admin.html',{'article_label': article_label,
                                                                 'classify_m': classify_m,
                                                                 'label_list_err': label_list_err,
                                                                 'label_now': label_now,
                                                                 'user_name': user_name,
                                                                 'label_m': label_m,
                                                                 'page_fen': page_fen,
                                                                 'p_b': p_b,
                                                                 'previous_page': previous_page,
                                                                 'next_page': next_page,
                                                                 'c': c,
                                                                 })
        else:
            return redirect('/myblog/login/')



#定义富文本DjangoUeditor,form
from django.forms import forms
from DjangoUeditor.forms import UEditorField
class TestUEditorForm(forms.Form):
    content = UEditorField('内容(不能为空)', width=720, height=400, toolbars="full", imagePath="images/", filePath="files/",
    upload_settings={"imageMaxSize":1204000},settings={})

#写博客
def create(request):
    cont_err = ''
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            form_m = TestUEditorForm()
            classify_cho = models.Classify.objects.all()
            label_list = models.Label.objects.all()

            return render(request, 'myblog/create.html', {'form_m': form_m,
                                                          'classify_cho':classify_cho,
                                                          'user_name': user_name,
                                                          'cont_err':cont_err,
                                                          'label_list':label_list,
                                                          })
        else:
            return redirect('/myblog/login/')

    if request.method == 'POST':
        article_content = ''
        cont = TestUEditorForm(request.POST)
        print(cont)                                             # 如果没有这行下一行会报错cleaned_data，原因尚不明确
        try:
            article_content = cont.cleaned_data['content']
        except:
            pass
        title = request.POST.get('title', None)
        introduce = request.POST.get('introduce', None)
        classify_cho_cont = request.POST.get('classify', None)
        label_cho = request.POST.getlist('label',None)   #多选要用getlist
        print(label_cho)
        if 0 < len(title) <= 32:
            if 0 < len(introduce) <= 64:
                if 0 < len(article_content):
                    if classify_cho_cont != None:
                        if 0 < len(label_cho):
                            art = models.Article.objects.create(title=title, introduce=introduce, content=article_content, classify_id=classify_cho_cont)
                            lab = models.Label.objects.filter(id__in=label_cho)
                            art.label.add(*lab)
                            return redirect('/myblog/index/')
                        else:
                            cont_err = '请选择标签'
                    else:
                        cont_err = '请选择类型'
                else:
                    cont_err = '内容格式不对'
            else:
                cont_err = '简介格式不对'
        else:
            cont_err = '标题格式不正确'

        user_name = request.session['username']
        form_m = TestUEditorForm()
        classify_cho = models.Classify.objects.all()
        label_list = models.Label.objects.all()
        return render(request, 'myblog/create.html', {'form_m': form_m,
                                                      'classify_cho': classify_cho,
                                                      'user_name': user_name,
                                                      'cont_err': cont_err,
                                                      'label_list': label_list,
                                                      })



#编辑博客
def edit(request,nid):
    cont_err = ''
    if request.method == 'GET':
        if request.session.get('login_state',None):
            user_name = request.session['username']
            article_edit = models.Article.objects.filter(id=nid).first()    #first传回的是一个对象不是query_set
            classify_selected = models.Article.objects.filter(id=nid).values('classify__classify')  #设置select默认选中
            classify_cho = models.Classify.objects.all()
            label_list = models.Label.objects.all()
            form_m = TestUEditorForm()
            return render(request, 'myblog/edit.html', {'article_edit': article_edit,
                                                        'form_m': form_m,
                                                        'classify_cho': classify_cho,
                                                        'classify_selected': classify_selected,
                                                        'user_name': user_name,
                                                        'cont_err':cont_err,
                                                        'label_list':label_list,
                                                        })
        else:
            return redirect('/myblog/login/')

    if request.method == 'POST':
        article_content = ''
        edit_cont = TestUEditorForm(request.POST)
        print(edit_cont)
        try:
            article_content = edit_cont.clean()['content']     #这里没有用cleaned_data
        except:
            pass
        title = request.POST.get('title', None)
        introduce = request.POST.get('introduce', None)
        classify_cho_cont = request.POST.get('classify', None)
        label_cho = request.POST.getlist('label',None)
        if 0<len(title)<=32:
            if 0<len(introduce)<=64:
                if 0<len(article_content):
                    if classify_cho_cont != None :
                        if 0 < len(label_cho):
                            # models.Article.objects.filter(id=nid).update(title=title,introduce=introduce,content=article_content,classify_id=classify_cho_cont)
                            # 必须下面这样的更新方式数据库的update字段才会自动更新↓
                            ud = models.Article.objects.get(id=nid)
                            ud.title = title
                            ud.introduce = introduce
                            ud.content = article_content
                            ud.classify_id = classify_cho_cont
                            ud.label.add(*label_cho)
                            ud.save()
                            return redirect('/myblog/admin/')
                        else:
                            cont_err = '请选择标签'
                    else:
                        cont_err = '请选择类型'
                else:
                    cont_err = '内容格式不对'
            else:
                cont_err = '简介格式不对'
        else:
            cont_err = '标题格式不正确'

        user_name = request.session['username']
        article_edit = models.Article.objects.filter(id=nid).first()  # first传回的是一个对象不是query_set
        classify_selected = models.Article.objects.filter(id=nid).values('classify__classify')  # 设置select默认选中
        classify_cho = models.Classify.objects.all()
        label_list = models.Label.objects.all()
        form_m = TestUEditorForm()
        return render(request, 'myblog/edit.html', {'article_edit': article_edit,
                                                    'form_m': form_m,
                                                    'classify_cho': classify_cho,
                                                    'classify_selected': classify_selected,
                                                    'user_name': user_name,
                                                    'cont_err':cont_err,
                                                    'label_list':label_list,
                                                    })



#删除博客
def delete(request):
    if request.method == 'GET':
        if request.session.get('login_state',None):
            nid = request.GET.get('nid',None)
            models.Article.objects.filter(id=nid).delete()
            return redirect('/myblog/admin/')
        else:
            return redirect('/myblog/login/')



#验证登录
def login(request):
    login_err = ''
    if request.method == 'GET':
        return render(request,'myblog/login.html',{'login_err':login_err})

    if request.method == 'POST':
        user = request.POST.get('user', None)
        password = request.POST.get('password', None)
        remeber = request.POST.get('remeber',None)
        print(remeber)
        obj = models.User.objects.filter(user=user, password=password).first()
        if obj:
            red = redirect('/myblog/admin/')
            # red.set_cookie('username',user)
            request.session['username'] = user
            request.session['login_state'] = True
            if remeber == None:
                request.session.set_expiry(0)          #()内代表在此秒数后失效，这里是关闭浏览器失效
            else:
                request.session.set_expiry(2592000)
            return red
        else:
            login_err = '输入有误'
            return render(request, 'myblog/login.html', {'login_err': login_err})



import json
def login_ajax(request):
    data_json = {'alt': True, 'errormes': None, 'data_m': None, }
    if request.method == 'POST':
        try:
            user = request.POST.get('user',None)
            password = request.POST.get('password',None)
            remeber = request.POST.get('remeber', None)
            # print(remeber)
            # print(type(remeber))
            obj = models.User.objects.filter(user=user,password=password).first()
            if obj :
                red = redirect('/myblog/admin/')
                # red.set_cookie('username',user)
                request.session['username'] = user
                request.session['login_state'] = True
                if remeber == 'false':
                    request.session.set_expiry(0)  # ()内代表在此秒数后失效，这里是关闭浏览器失效
                else:
                    request.session.set_expiry(2592000)
            else:
                data_json['alt'] = False
                data_json['errormes'] = '输入有误'
        except:
            data_json['alt'] = False
            data_json['errormes'] = '服务器错误'
        return HttpResponse(json.dumps(data_json))



#注销登录
def logout(request):
    if request.method =='GET':
        request.session.clear()
        return redirect('/myblog/index/')



def test(request):
    # obj1 = models.Classify.objects.get(id=1)
    # obj1_1 = obj1.article_set.all()
    # print(obj1_1)
    # obj1_2 = models.Article.objects.filter(classify=obj1)
    # print(obj1_2)
    # obj2 = models.Article.objects.all()
    # print(obj2)
    # for i in obj2:
    #     print(i)
    #     print(i.classify.classify)
    #     print(i.label.all())
    # return render(request, 'myblog/test.html', {'obj2':obj2,
    #                                             'obj1':obj1})
    # return HttpResponse('ok')
    if request.method == "GET":

        return render(request, 'myblog/handsome.html')

    if request.method == "POST":
        # se1 = request.POST.get('se1', None)
        # print(se1)
        # print(se1.split(','))
        ch1 = request.POST.get('ch1', None)
        ch2 = request.POST.get('ch2', None)
        ch3 = request.POST.get('ch3', None)
        ch4 = request.POST.get('ch4', None)
        print(ch4)
        ch5 = request.POST.get('ch3,ch2', None)
        print(ch5)
        print(ch1,ch2,ch3)
    return render(request, 'myblog/test.html')