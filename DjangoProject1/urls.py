"""
URL configuration for DjangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.views.static import serve

import HelloWorld.views
from DjangoProject1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # nameはURLの名前を付け、テンプレートやコード内でのURLを参照やすいするためのもの
    path('', HelloWorld.views.index, name='index'),
    path('download1/', HelloWorld.views.download_file1),
    path('download2/', HelloWorld.views.download_file2),
    path('download3/', HelloWorld.views.download_file3),
    path('get', HelloWorld.views.get_test),
    path('post', HelloWorld.views.post_test),
    path('tologin/', HelloWorld.views.to_login),
    path('tocourse/', HelloWorld.views.to_course),
    path('book/list', HelloWorld.views.bookList),
    path('book/list2', HelloWorld.views.bookList2),
    path('book/preAdd', HelloWorld.views.preAdd),
    path('book/preAdd2', HelloWorld.views.preAdd2),
    path('book/preAdd3', HelloWorld.views.preAdd3),
    path('book/add', HelloWorld.views.add),
    path('book/update', HelloWorld.views.update),
    path('book/preUpdate/<int:id>', HelloWorld.views.preUpdate),
    path('book/delete/<int:id>', HelloWorld.views.delete),
    path('transfer2/', HelloWorld.views.transfer2),
    path('login', HelloWorld.views.login),
    path('toupload/', HelloWorld.views.to_upload),
    path('upload', HelloWorld.views.upload),
    path('student/list', HelloWorld.views.List.as_view()),
    path('student/<int:id>', HelloWorld.views.Detail.as_view()),
    path('student/create', HelloWorld.views.Create.as_view()),
    path('student/update/<int:pk>', HelloWorld.views.Update.as_view()),
    path('student/delete/<int:pk>', HelloWorld.views.Delete.as_view()),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('order/', include(('order.urls', 'user'), namespace='order')),
    path('redirectTo', RedirectView.as_view(url='index/')),
    path('blog/<int:id>', HelloWorld.views.blog),
    # Auth
    path('authtoLogin/',HelloWorld.views.authto_login),
    path('auth/login',HelloWorld.views.authlogin),
    path('auth/setPwd',HelloWorld.views.setPwd),
    path('auth/logout',HelloWorld.views.logout),
    path('auth/index',HelloWorld.views.to_index),
    path('toRegister/', HelloWorld.views.to_register),
    path('auth/register', HelloWorld.views.register),
    path('blog2/<int:year>/<int:month>/<int:day>/<int:id>', HelloWorld.views.blog2),
    re_path('blog3/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})',HelloWorld.views.blog3),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT},name='media')
]
