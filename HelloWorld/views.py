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
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from DjangoProject1 import settings
from HelloWorld import utils
from HelloWorld.forms import StudentForm, BookInfoForm, BookInfoModelForm, ImageConversionForm
from HelloWorld.models import StudentInfo, BookInfo, BookTypeInfo, AccountInfo


class Person:
    name = None
    age = None
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Create your views here.
# ホームページのリクエスト(request)を処理し、レスポンス(response)を返す
def index(request):
    logs = []
    lang = utils.get_current_language()
    print("Request Method:")

    # コンテキストに翻訳文字列を追加
    context_value = {
        "logs": logs,
        "hello": utils.get_translated_text(lang, "hello"),
        "mbti": utils.get_translated_text(lang, "mbti"),
        "Navbar": utils.get_translated_text(lang, "Navbar"),
        "book": utils.get_translated_text(lang, "book"),
        "File_selector": utils.get_translated_text(lang, "File_selector"),
        "transfer": utils.get_translated_text(lang, "transfer"),
        "admin": utils.get_translated_text(lang, "admin"),
        "Information_Output": utils.get_translated_text(lang, "Information_Output"),
        "no_Output": utils.get_translated_text(lang, "no_Output"),
        # "footer": footer,
        "personality": utils.get_translated_text(lang, "personality"),
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
    file = open(file_path, 'rb')
    response = HttpResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file1.zip'
    return response

def download_file2(request):
    file = open(file_path, 'rb')
    response = StreamingHttpResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file2.zip'
    return response

def download_file3(request):
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=file3.zip'
    return response

def get_test(request):
    print(request.method)
    # 属性
    print(request.content_type)
    print(request.content_params)
    print(request.COOKIES)
    print(request.scheme)
    # メソッド
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
        # 特定のフォルダにバイナリモードでファイルを開く
        f=open(os.path.join(r"F:\code\DjangoProject1\myFile",myFile.name),"wb+")
        # ファイルをチャンクごとに書き込む
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse("upload ok!")
    else:
        return HttpResponse("no file for upload!")

#  学生リストを表示（ページネーション付き）
class List(ListView):
    template_name = "student/list.html"
    extra_context = {"title":"Students List"}
    queryset = StudentInfo.objects.all()
    paginate_by = 5
    context_object_name = "student_list"

#  学生の詳細を表示
class Detail(DetailView):
    template_name = "student/detail.html"
    extra_context = {"title": "Students Detail"}
    model = StudentInfo
    context_object_name = "student"
    pk_url_kwarg = "id"

# 学生情報の更新
class Update(UpdateView):
    template_name = 'student/update.html'
    extra_context = {"title": "Update Student infomation"}
    model = StudentInfo
    form_class = StudentForm
    success_url = "/student/list"

# 新しい学生情報を作成
class Create(CreateView):
    template_name = 'student/create.html'

    extra_context = {"title": "Create Student infomation"}
    form_class = StudentForm
    success_url = "/student/list"

#  学生情報を削除
class Delete(DeleteView):
    template_name = 'student/delete.html'
    extra_context = {"title": "Delete Student infomation"}
    model = StudentInfo
    context_object_name = "student"
    success_url = "/student/list"

def to_course(request):
    return render(request, 'course.html')

#  書籍リストを表示
def bookList(request):
    lang = utils.get_current_language()
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
    print("総記錄数" ,BookInfo.objects.count())
    context_value = {
        "title" : "書籍リスト" ,
        "bookList":bookList,
        "Navbar": utils.get_translated_text(lang, "Navbar"),
    }
    return render(request, 'book/List.html', context=context_value)

def bookList2(request):
    #正常查詢
    book: BookInfo = BookInfo.objects.filter(id=2).first()
    print(book.bookName, book.bookType.bookTypeName)

    #反向查詢
    bookType: BookTypeInfo = BookTypeInfo.objects.filter(id=1).first()
    print(bookType.bookinfo_set.first().bookName)

    context_value = {"title": "書籍リスト"}
    return render(request, 'book/List.html', context=context_value)

def preAdd(request):

    bookTypeList =  BookTypeInfo.objects.all()
    print(bookTypeList)
    context_value = {"title" : "書籍の追加" ,"bookTypeList":bookTypeList}
    return render(request, "book/add.html", context_value)

def preAdd2(request):
    form = BookInfoForm()

    context_value = {"title" : "書籍の追加2" ,"form": form}
    return render(request, "book/add2.html", context_value)

def preAdd3(request):
    form = BookInfoModelForm()

    context_value = {"title": "書籍の追加3", "form": form}
    return render(request, "book/add2.html", context_value)

#書籍の編集
def preUpdate(request,id):
    print("id:",id)
    book = BookInfo.objects.get(id=id)
    print(book.bookName)

    bookTypeList = BookTypeInfo.objects.all()
    print(bookTypeList)
    context_value = {"title": "書籍の編集", "bookTypeList": bookTypeList, "book":book}
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

#  書籍情報を更新
def update(request):
    book = BookInfo()
    book.id = request.POST.get("id")
    book.bookName = request.POST.get("bookName")
    book.price = request.POST.get("price")
    book.publishDate = request.POST.get("publishDate")
    book.bookType_id = request.POST.get("bookType_id")
    book.save()
    return bookList(request)

#  書籍を削除
def delete(request,id):
    BookInfo.objects.get(id=id).delete()
    # BookInfo.objects.filter(price__gte=90).delete()
    return bookList(request)

#  ユーザー登録ページを表示
def to_register(request):
    return render(request,'auth/register.html')

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    #檢測用戶名是否存在
    result = User.objects.filter(username=username)
    if result:
        return render(request,'auth/register.html',context={"errorfinfo":"このユーザー名は既に存在します"})
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
        auth.login(request, resUser)
        return render(request, 'auth/index.html')
    else:
        return render(request, 'auth/login.html',
                  context={"errorInfo": "ユーザー名またはパスワードが間違っています", "username":
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
                          context={"errorfinfo": "パスワードが間違っています","newPwd":newPwd})
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
        print("エラー：",e)
        transaction.savepoint_rollback(sid)

    return HttpResponse("transfer ok")

