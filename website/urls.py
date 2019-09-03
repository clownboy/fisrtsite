"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include,re_path
from firstapp.views import index,window,register,userlogin,userlogout,onnote,mynote,account,headupload,deletenote,comment,mypaper,search,emailset,passwordset
from django.contrib.staticfiles.views import serve
from firstapp import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from firstapp.api import getcomment
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', index,name='index'),
    path('register', register,name='register'),
    path('userlogin', userlogin,name='userlogin'),
    path('userlogout', userlogout,name='userlogout'),
    re_path(r'^onnote', onnote,name='onnote'),
    re_path(r'^window$', window,name='window'),
    re_path(r'^emailset$', emailset,name='emailset'),
    path('headupload', headupload,name='headupload'),
    path('passwordset', passwordset,name='passwordset'),
    re_path(r'^search', search,name='search'),
    re_path(r'^mypaper', mypaper,name='mypaper'),
    re_path(r'^api/getcomment', getcomment,name='comment'),
    re_path(r'^comment', comment,name='comment'),
    re_path(r'^mynote', mynote,name='mynote'),
    re_path(r'^deletenote', deletenote,name='deletenote'),
    path('account', account,name='account'),
    path('favicon.ico', serve, {'path': 'images/favicon.ico'}),
    path('api/v1/', include('website.version_1')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
