from django.urls import path
from authorization import views,ocr

urlpatterns = [
    path('authorize',views.authorize),
    path('wxlogin',views.wxlogin),
    path('index',views.index),
    path('mynote',views.mynote),
    path('logout',views.logout),
    path('deletenote',views.deletenote),
    path('onnote',views.onnote),
    path('noteonline',ocr.noteonline),
]
