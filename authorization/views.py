from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.conf import settings
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from firstapp.models import Comment,Userinfo,Artical
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from django.utils.timezone import utc
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from firstapp.forms import booknoteform
import datetime
class ArticalSerializer(serializers.ModelSerializer):
    noter = serializers.SerializerMethodField()
    noteinfo = serializers.SerializerMethodField()
    notetime = serializers.SerializerMethodField()
    def get_notetime(self, obj):
        if obj.notetime:
           notetime = obj.notetime + datetime.timedelta(hours=8)
           notetime = datetime.datetime.strftime(notetime,'%Y-%m-%d %H:%M:%S')
           return notetime
    def get_noter(self, obj):
        if obj.noter:
           noter=obj.noteinfo.nickname
           return noter
    def get_noteinfo(self, obj):
        if obj.noteinfo:
           noteinfo = str(obj.noteinfo.headlogo)
           return noteinfo
    class Meta:
        model = Artical
        fields = "__all__"
        depth = 1
class UserSerializer(serializers.ModelSerializer):
    userid = serializers.SerializerMethodField()
    def get_userid(self, obj):
        if obj.belong_to_id:
           userid = obj.belong_to_id
           return userid
    class Meta:
        model = Userinfo
        fields = "__all__"
class MynoteSerializer(serializers.ModelSerializer):
    noter = serializers.SerializerMethodField()
    notetime = serializers.SerializerMethodField()
    def get_notetime(self, obj):
        if obj.notetime:
           notetime = obj.notetime + datetime.timedelta(hours=8)
           notetime = datetime.datetime.strftime(notetime,'%Y-%m-%d %H:%M:%S')
           return notetime
    def get_noter(self, obj):
        if obj.noter.username:
           noter=obj.noter.username
           return noter
    class Meta:
        model = Artical
        fields = "__all__"
        depth = 1
@csrf_exempt
@api_view(['GET'])
def index(request):
    if request.method =='GET':
       today = datetime.datetime.utcnow().replace(tzinfo=utc).date()
       articals = Artical.objects.all().order_by("-notetime")[:3]
       serializer = ArticalSerializer(articals,many=True)
       return JsonResponse(data=serializer.data,safe=False)
@csrf_exempt
@api_view(['POST'])
def onnote(request):
    if request.method =='POST':
       noter = request.session['userID']
       noteid = request.POST.get("id")
       form = booknoteform(request.POST)
       if not noteid:
            if form.is_valid():
                bookname = form.cleaned_data.get("bookname")
                author = form.cleaned_data.get("author")
                pagenumber = form.cleaned_data.get("pagenumber")
                content = form.cleaned_data.get("content")
                notetime = datetime.datetime.utcnow().replace(tzinfo=utc)
                new_note = Artical.objects.create(bookname=bookname,author=author,pagenumber=pagenumber,content=content,notetime=notetime,noter_id=noter,noteinfo_id=noter)
                new_note.save()
                return JsonResponse(data='ok',safe=False)
            else:
                return JsonResponse(data='error',safe=False)
       elif form.is_valid():
            bookname = form.cleaned_data.get("bookname")
            author = form.cleaned_data.get("author")
            pagenumber = form.cleaned_data.get("pagenumber")
            content = form.cleaned_data.get("content")
            Artical.objects.filter(id=noteid).update(bookname=bookname,author=author,pagenumber=pagenumber,content=content)
            return JsonResponse(data='ok',safe=False)
       else:
            return JsonResponse(data='error',safe=False)
@csrf_exempt
@api_view(['DELETE'])
def deletenote(request):
    username = request.session['userID']
    id=request.GET['d']
    if Artical.objects.filter(id=id,noter=username):
      Artical.objects.filter(id=id).delete()
      return JsonResponse(data='删除成功',safe=False)
@csrf_exempt
@api_view(['GET'])
def mynote(request):
    if request.method =='GET':
       user = request.session['userID']
       articals = Artical.objects.filter(noter=user).order_by("-notetime")
       serializer = MynoteSerializer(articals,many=True)
       return JsonResponse(data=serializer.data,safe=False)
@csrf_exempt
@api_view(['GET'])
def logout(request):
    if request.method =='GET':
      openid = request.session['open_id']
      Userinfo.objects.filter(open_id=openid).update(open_id="null")
      return JsonResponse(data="退出成功",safe=False)
@csrf_exempt
@api_view(['POST'])
def wxlogin(request):
  if request.method =='POST':
    open_id = request.session['open_id']
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user:
          Userinfo.objects.filter(belong_to_id=user.id).update(open_id=open_id)
          request.session['username'] = username
          request.session['userid'] = user.id
          return JsonResponse(data='ok',safe=False)
        else:
          return JsonResponse(data='error',safe=False)

# def session2(request):
#     print('session',request.session.items())
#     response=['data']
#     return JsonResponse(response,safe=False)
def c2s(appid,code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'%(appid,settings.WX_APP_SECRET,code)
    url = API+'?'+params
    response = requests.get(url=url)
    data = json.loads(response.text)
    return data

@csrf_exempt
def authorize(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appID').strip()
    # if not code or not app_id:
    #     response['message'] = 'not ok'
    #     return response
    data = c2s(app_id,code)
    openid = data.get('openid')
    request.session['open_id'] = openid
    if not Userinfo.objects.filter(open_id=openid):
        return JsonResponse(data="error",safe=False)
    else:
        user = Userinfo.objects.get(open_id=openid)
        userid = user.belong_to_id
        request.session['userID'] =userid
        request.session['is_autherized'] = True
        userinfo = Userinfo.objects.filter(open_id=openid)
        serializer = UserSerializer(userinfo,many=True)
        return JsonResponse(data=serializer.data,safe=False)
