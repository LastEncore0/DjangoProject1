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
    path('index/', HelloWorld.views.index),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('order/', include(('order.urls', 'user'), namespace='order')),
    path('redirectTo', RedirectView.as_view(url='index/')),
    path('blog/<int:id>', HelloWorld.views.blog),
    path('blog2/<int:year>/<int:month>/<int:day>/<int:id>', HelloWorld.views.blog2),
    re_path('blog3/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})',HelloWorld.views.blog3),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT},name='media')
]
