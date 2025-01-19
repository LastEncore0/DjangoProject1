import json
import os
import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import connection, transaction
from django.db.backends.utils import CursorDebugWrapper
from django.db.models import Sum, F
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.utils.translation import get_language, activate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from DjangoProject1 import settings
from HelloWorld.forms import StudentForm, BookInfoForm, BookInfoModelForm, ImageConversionForm
from HelloWorld.models import StudentInfo, BookInfo, BookTypeInfo, AccountInfo


class Person:
    name = None
    age = None
    def __init__(self, name, age):
        self.name = name
        self.age = age

def get_current_language():
    """ 現在の言語を取得し、存在しない場合はデフォルト (ja) に設定する """
    lang = get_language()
    if lang not in ["ja", "en", "zh-hans"]:  # 定義済みの言語リスト
        lang = "ja"  # デフォルトは日本語
    return lang

def set_language(request):
    lang = request.GET.get("lang", "ja")
    if lang not in ["ja", "en", "zh-hans"]:
        lang = "ja"

    activate(lang)  # 新しい言語に切り替わる
    print("Language:", lang)
    response = redirect(request.META.get("HTTP_REFERER", "/"))  # 重定向回前一个页面
    response.set_cookie("django_language", lang)  # 设置 cookie，记住语言
    print("Cookie:", response.cookies)
    return response

# 翻訳Jsonを読み取る
with open("translations.json", encoding="utf-8") as f:
    translations = json.load(f)

def get_translated_text(lang, key):
    """  获取翻译内容，如果不存在则使用日语（ja） """
    return translations.get(lang, {}).get(key, translations["ja"].get(key, key))


# Create your views here.
# ホームページのリクエスト(request)を処理し、レスポンス(response)を返す
def index(request):

    lang = get_current_language()
    print("Request Method:")

    # コンテキストに翻訳文字列を追加
    context_value = {
        "hello": get_translated_text(lang, "hello"),
        "mbti": get_translated_text(lang, "mbti"),
        "Navbar": get_translated_text(lang, "Navbar"),
        "book": get_translated_text(lang, "book"),
        # "footer": footer,
        "date": datetime.datetime.now()
    }

    if request.method == "POST":
        print("Received POST with data:", request.POST)
        form = ImageConversionForm(request.POST)
        if form.is_valid():
            conversion = form.save()
            logs = conversion.convert_images()
            context_value.update({"form": form, "logs": logs})
            return render(request, "index.html", context_value)

    else:
        form = ImageConversionForm()  # 确保 GET 请求也有 `form`
    context_value["form"] = form
    print("context_value:",context_value)
    return render(request, "index.html", context_value)

def blog(request, id):
    if id == 0:
        return redirect("/s1/error.html")
    else:
        return HttpResponse("id:" + str(id))
def blog2(request, id, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day) + '/'  +"id:" + str(id))
def blog3(request, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day))

# 定義文件路徑
file_path = r"E:\ae files\example.zip"

def download_file1(request):
    file = open(file_path, 'rb') #打開文件
    response = HttpResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file1.zip'
    return response

def download_file2(request):
    file = open(file_path, 'rb') #打開文件
    response = StreamingHttpResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file2.zip'
    return response

def download_file3(request):
    file = open(file_path, 'rb') #打開文件
    response = FileResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file3.zip'
    return response

def get_test(request):
    print(request.method)
    # 常用属性
    print(request.content_type)
    print(request.content_params)
    print(request.COOKIES)
    print(request.scheme)
    # 常用方法
    print(request.is_secure())
    print(request.get_host())
    print(request.get_full_path())

    print(request.GET.get("name"))
    print(request.GET.get("pwd"))
    return HttpResponse("got test ok")

def post_test(request):
    print(request.method)
    print(request.POST.get("name"))
    print(request.POST.get("pwd"))
    return HttpResponse("post test ok")

def to_login(request):
    return render(request, 'login.html')

def login(request):
    username = request.POST.get("username")
    pwd = request.POST.get("pwd")

    if username == "baka9" and pwd == "123456":
        request.session["username"] = username
        print("session username:",request.session.get("username"))
        return render(request, 'main.html')
    else:
        context_value = {"error_info": "username or password is wrong!"}
        return render(request,'login.html',context=context_value)

def to_upload(request):
    return render(request, 'upload.html')

def upload(request):
    myFile = request.FILES.get("myfile",None)
    if myFile:
        # 打開特定的文件進行二進制操作
        f=open(os.path.join(r"F:\code\DjangoProject1\myFile",myFile.name),"wb+")
        # 分塊寫入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse("upload ok!")
    else:
        return HttpResponse("no file for upload!")

class List(ListView):
    template_name = "student/list.html"
    extra_context = {"title":"Students List"}
    queryset = StudentInfo.objects.all()
    paginate_by = 5
    context_object_name = "student_list"

class Detail(DetailView):
    template_name = "student/detail.html"
    extra_context = {"title": "Students Detail"}
    model = StudentInfo
    context_object_name = "student"
    pk_url_kwarg = "id"

class Update(UpdateView):
    template_name = 'student/update.html'
    extra_context = {"title": "Update Student infomation"}
    model = StudentInfo
    form_class = StudentForm
    success_url = "/student/list"

class Create(CreateView):
    template_name = 'student/create.html'

    extra_context = {"title": "Create Student infomation"}
    form_class = StudentForm
    success_url = "/student/list"

class Delete(DeleteView):
    template_name = 'student/delete.html'
    extra_context = {"title": "Delete Student infomation"}
    model = StudentInfo
    context_object_name = "student"
    success_url = "/student/list"

def to_course(request):
    return render(request, 'course.html')

def bookList(request):
    lang = get_current_language()
    bookList = BookInfo.objects.all()

    # bookList = BookInfo.objects.raw("select * from t_book where price>%s",params=[10])
    # cursor: CursorDebugWrapper = connection.cursor()
    # cursor.execute("select * from t_book where price>90")
    # print(cursor.fetchone())
    # bookList = BookInfo.objects.extra(where=["price>10"])
    # t = BookInfo.objects.filter(id=2).count()
    # print(t)
    # booklist = BookInfo.objects.order_by("-id")
    # print(booklist)
    # r = BookInfo.objects.values("bookType").annotate(Sum("price"))
    # print(r)
    p = Paginator(bookList,2)
    bookListPage = p.page(1)
    print("縂記錄數" ,BookInfo.objects.count())
    context_value = {
        "title" : "圖書列表" ,
        "bookList":bookList,
        "Navbar": get_translated_text(lang, "Navbar"),
    }
    return render(request, 'book/List.html', context=context_value)

def bookList2(request):
    #正常查詢
    book: BookInfo = BookInfo.objects.filter(id=2).first()
    print(book.bookName, book.bookType.bookTypeName)

    #反向查詢
    bookType: BookTypeInfo = BookTypeInfo.objects.filter(id=1).first()
    print(bookType.bookinfo_set.first().bookName)

    context_value = {"title": "圖書列表"}
    return render(request, 'book/List.html', context=context_value)

def preAdd(request):

    bookTypeList =  BookTypeInfo.objects.all()
    print(bookTypeList)
    context_value = {"title" : "圖書添加" ,"bookTypeList":bookTypeList}
    return render(request, "book/add.html", context_value)

def preAdd2(request):
    form = BookInfoForm()

    context_value = {"title" : "圖書添加2" ,"form": form}
    return render(request, "book/add2.html", context_value)

def preAdd3(request):
    form = BookInfoModelForm()

    context_value = {"title": "圖書添加3", "form": form}
    return render(request, "book/add2.html", context_value)


def preUpdate(request,id):
    print("id:",id)
    book = BookInfo.objects.get(id=id)
    print(book.bookName)

    bookTypeList = BookTypeInfo.objects.all()
    print(bookTypeList)
    context_value = {"title": "圖書修改", "bookTypeList": bookTypeList, "book":book}
    return render(request, "book/edit.html", context_value)

def add(request):
    # print(request.POST.get("bookName"))
    # print(request.POST.get("price"))
    # print(request.POST.get("publishDate"))
    # print(request.POST.get("bookType_id"))
    book = BookInfo()
    book.bookName = request.POST.get("bookName")
    book.price = request.POST.get("price")
    book.publishDate = request.POST.get("publishDate")
    book.bookType_id = request.POST.get("bookType")
    book.save()
    print("id:",book.id)
    return bookList(request)

def update(request):
    book = BookInfo()
    book.id = request.POST.get("id")
    book.bookName = request.POST.get("bookName")
    book.price = request.POST.get("price")
    book.publishDate = request.POST.get("publishDate")
    book.bookType_id = request.POST.get("bookType_id")
    book.save()
    return bookList(request)

def delete(request,id):
    BookInfo.objects.get(id=id).delete()
    # BookInfo.objects.filter(price__gte=90).delete()
    return bookList(request)

def to_register(request):
    return render(request,'auth/register.html')

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    #檢測用戶名是否存在
    result = User.objects.filter(username=username)
    if result:
        return render(request,'auth/register.html',context={"errorfinfo":"該用戶名已存在"})
    User.objects.create_user(username=username,password=password)
    return render(request,'auth/login.html')

def authto_login(request):
    return render(request,'auth/login.html')

def authlogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    resUser = auth.authenticate( request,username=username,password=password)
    if resUser and resUser.is_active:
        print(resUser, type(resUser))
    # 用户登录成功之后（返回给客户端登录的凭证或者说是令牌、随机字符串）
        auth.login(request, resUser)
        return render(request, 'auth/index.html')
    else:
        return render(request, 'auth/login.html',
                  context={"errorInfo": "用户名或者密码错误", "username":
                      username, "password": password})

def logout(request):
    auth.logout(request)
    return render(request,'auth/index.html')

def to_index(request):

    return render(request,'auth/index.html')

def setPwd(request):

    if request.method == "POST":
        oldPwd = request.POST.get("oldPwd")
        newPwd = request.POST.get("newPwd")
        isRight = request.user.check_password(oldPwd)
        if not isRight:
            return render(request,'auth/setPwd.html',
                          context={"errorfinfo": "原密码错误","newPwd":newPwd})
        request.user.set_password(newPwd)
        request.user.save()
        return render(request,'auth/index.html')
    return render(request,'auth/setPwd.html')


@transaction.atomic
def transfer2(request):
    # 開啓事務
    sid = transaction.savepoint()
    try:
        a1 = AccountInfo.objects.filter(user='baka9')
        a1.update(account=F('account') + 100)

        a2 = AccountInfo.objects.filter(user='baqkan')
        a2.update(account=F('account') - 100)

        #提交事務
        transaction.savepoint_commit(sid)
    except Exception as e:
        print("異常信息：",e)
        transaction.savepoint_rollback(sid)

    return HttpResponse("transfer ok")

