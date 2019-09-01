from django.db import models
from django.conf import settings
from django.utils import timezone

class Userinfo(models.Model):
    belong_to = models.OneToOneField(settings.AUTH_USER_MODEL,primary_key=True,related_name='profile',on_delete=models.CASCADE,parent_link=True)
    open_id = models.CharField(max_length=32)
    nickname = models.CharField(max_length=256,null='佚名',default='佚名',blank='佚名')
    headlogo = models.ImageField(upload_to='images',blank=True,null=True,default='/static/images/headlogo.png')

class Artical(models.Model):
    bookname = models.CharField(null=True,blank=True,max_length=100)
    author = models.CharField(null='无名',blank='无名',max_length=100)
    content = models.TextField(null=True,blank=True,max_length=1024)
    pagenumber = models.IntegerField(null='0',blank='0')
    notetime = models.DateTimeField(blank=True,default=None)
    noter = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='notelist',on_delete=models.CASCADE,parent_link=True,null=True,blank=True)
    noteinfo = models.ForeignKey(Userinfo,related_name='noterlist',on_delete=models.CASCADE,parent_link=True,null=True,blank=True)
    class meta:
        ordering = ['-notetime']

class Comment(models.Model):
    talk = models.CharField(null=True,blank=True,max_length=240)
    talker = models.ForeignKey(Userinfo,related_name='talker_userinfo',on_delete=models.CASCADE,parent_link=True,null=True,blank=True)
    artical = models.ForeignKey(Artical,related_name='artical_comment',on_delete=models.CASCADE,parent_link=True,null=True,blank=True)
    talktime = models.DateTimeField(blank=True,default=None)
