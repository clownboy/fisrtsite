from django.shortcuts import render,HttpResponse, redirect
from django.template import Context,Template,RequestContext
from firstapp.forms import RegisterForm,LoginForm,booknoteform,Emailform
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .models import Artical,Userinfo,Comment
from django.utils.timezone import utc
from django.core.paginator import Paginator
import json
import datetime
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def passwordset(request):
    password = request.POST.get('repassword')
    user=User.objects.get(id=request.user.id)
    user.set_password(password)
    user.save()
    return JsonResponse({'ok':'ok'})
@login_required
def emailset(request):
    email=Emailform(request.POST)
    user=request.user.id
    if email.is_valid():
       email=email.cleaned_data.get("email")
       User.objects.filter(id=user).update(email=email)
       send_mail('万物之光', '收到邮件表示邮箱绑定成功，你可以通过此邮箱找回密码。若使用过程中有遇到问题或有好的建议，可以通过邮箱联系我。', 'dk_dante@qq.com',
       [email], fail_silently=False)
       return JsonResponse({'ok':'ok'})
    error=email.errors
    return JsonResponse({'error':error})
def search(request):
    if request.method =='GET':
       user=request.user.id
       user = Userinfo.objects.get(belong_to_id=user)
       bookname = request.GET['bookname']
       articals = Artical.objects.filter(bookname=bookname)
       return render(request, 'window.html', {'articals':articals,'user':user})
@login_required
def comment(request):
    if request.method =='POST':
      talk = request.POST.get('talk','收藏')
      artical = request.POST.get('artical')
      talker_id = request.user.id
      com = Comment.objects.create(talk=talk,talker_id=talker_id,artical_id=artical,talktime=datetime.datetime.utcnow().replace(tzinfo=utc))
      com.save
      return JsonResponse({'resp':'ok'})
def deletenote(request):
    id=request.body
    if request.method =='POST':
      Artical.objects.filter(id=id).delete()
      return JsonResponse({'resp':'ok'})
def account(request):
    if request.method =='POST':
        nickname = request.POST.get('nickname', '')
        belong_to=request.user.id
        if not nickname:
            nickname="佚名"
        if not Userinfo.objects.filter(belong_to=belong_to):
            userinfo = Userinfo.objects.create(nickname=nickname,belong_to_id=belong_to)
            userinfo.save()
            return JsonResponse({'resp':'ok'})
        Userinfo.objects.filter(belong_to=belong_to).update(nickname=nickname)
        return JsonResponse({'nickname':nickname})
def headupload(request):
    if request.method =='POST':
        belong_to = request.user.id
        pic = request.FILES["headlogo"]
        im_pic = Image.open(pic)
        im_pic=im_pic.resize((160,160))
        creattime=datetime.datetime.strftime(datetime.datetime.utcnow().replace(tzinfo=utc),'%Y%m%d%H%M%S')
        headlogo='media/images/'+str(belong_to)+'_'+str(creattime)+"."+"png"
        im_pic.save(headlogo,"png")
        if not Userinfo.objects.filter(belong_to=belong_to):
            userinfo = Userinfo.objects.create(headlogo=headlogo,belong_to_id=belong_to)
            userinfo.save()
            return redirect('/mynote?page=1')
        Userinfo.objects.filter(belong_to=belong_to).update(headlogo=headlogo)
        return redirect('/mynote?page=1')
@login_required
def mynote(request):
    if request.method =='GET':
        noter=request.user.id
        articals={}
        user = Userinfo.objects.get(belong_to_id=noter)
        if Artical.objects.filter(noter_id=noter):
           articals =Artical.objects.filter(noter_id=noter).order_by("-notetime")
           page_robot = Paginator(articals,10)
           page_num = request.GET.get('page')
           if not page_num:
             return redirect('/mynote?page=1')
           articals = page_robot.page(page_num)
           num_pages   = page_robot.num_pages
           countpage = range(1,num_pages+1)
           return render(request, 'window.html', {'articals':articals,'user':user,'countpage':countpage,'num_pages':num_pages})
        return render(request, 'window.html', {'articals':articals,'user':user})
@login_required
def mypaper(request):
    if request.method =='GET':
        talker=request.user.id
        user = Userinfo.objects.get(belong_to_id=talker)
        articals={}
        if Comment.objects.filter(talker=talker):
           paper = Comment.objects.filter(talker=talker).prefetch_related('artical').order_by("-talktime")
           page_robot = Paginator(paper,10)
           page_num = request.GET.get('page')
           if not page_num:
             return redirect('/mypaper?page=1')
           papers = page_robot.page(page_num)
           num_pages = page_robot.num_pages
           countpage = range(1,num_pages+1)
           return render(request, 'window.html', {'papers':papers,'user':user,'countpage':countpage,'num_pages':num_pages})
        return render(request, 'window.html', {'articals':articals,'user':user})

def index(request):
    if request.method =='GET':
        form = RegisterForm()
        articals={}
        today = datetime.datetime.utcnow().replace(tzinfo=utc).date()
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if Artical.objects.filter(notetime__gt=today):
           articals=Artical.objects.filter(notetime__gt=today).order_by("-notetime")
           return render(request, 'index.html', {'form':form,'articals':articals})
        return render(request, 'index.html', {'form':form,'articals':articals})

@login_required
def window(request):
    if request.method =='GET':
       noter=request.user.id
       today = datetime.datetime.utcnow().replace(tzinfo=utc).date()
       user = Userinfo.objects.get(belong_to_id=noter)
       articals={}
       if Artical.objects.filter(notetime__gt=today):
          articals = Artical.objects.filter(notetime__gt=today).order_by("-notetime")
          return render(request, 'window.html', {'articals':articals,'user':user})
       return render(request, 'window.html', {'articals':articals,'user':user})
@login_required
def onnote(request):
    if request.method =='POST':
        noteid = request.POST.get("id")
        form = booknoteform(request.POST)
        noter = request.user.id
        if not noteid:
            if form.is_valid():
                bookname = form.cleaned_data.get("bookname")
                author = form.cleaned_data.get("author")
                pagenumber = form.cleaned_data.get("pagenumber")
                content = form.cleaned_data.get("content")
                if form.cleaned_data.get("notetime") is None:
                   notetime = datetime.datetime.utcnow().replace(tzinfo=utc)
                else: notetime = form.cleaned_data.get("notetime")
                new_note = Artical.objects.create(bookname=bookname,author=author,pagenumber=pagenumber,content=content,notetime=notetime,noter_id=noter,noteinfo_id=noter)
                new_note.save()
                return redirect('http://127.0.0.1:8000/mynote?page=1')
            else:
                resp=form.errors
                print(resp)
                return JsonResponse({'resp':resp})
        elif form.is_valid():
            bookname = form.cleaned_data.get("bookname")
            author = form.cleaned_data.get("author")
            pagenumber = form.cleaned_data.get("pagenumber")
            content = form.cleaned_data.get("content")
            Artical.objects.filter(id=noteid).update(bookname=bookname,author=author,pagenumber=pagenumber,content=content)
            return redirect('http://127.0.0.1:8000/mynote?page=1')
        else:
            resp=form.errors
            print(resp)
            return JsonResponse({'resp':resp})
def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            from django.contrib.auth.models import User
            new_user = User.objects.create_user(username=username,password=password)
            new_user.save()
            Userinfo.objects.create(belong_to_id=new_user.id).save()
            resp='success'
            login(request,new_user)
            return JsonResponse({'resp':'success'})
        else:
            resp=form.errors
            print(resp)
            return JsonResponse({'resp':resp})

def userlogin(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return JsonResponse({'resp':'success'})
        else:
            return JsonResponse({'resp':'用户名或密码错误'})
def userlogout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000')# Redirect to a success page.
