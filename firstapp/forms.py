from django.forms import ModelForm
from django import forms
from .models import Artical
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def username_validator(username):
    if User.objects.filter(username=username):
        raise ValidationError('用户名已存在')
    return username
class LoginForm(forms.Form):
    username = forms.CharField(max_length=32,
    error_messages={'required': '请输入用户名'},)
    password = forms.CharField(max_length=32, min_length=6,
    error_messages={'required': '请输入密码','min_length':'密码至少为6位'})      # 密码

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32,
    error_messages={'required': '请输入用户名'},
    validators=[username_validator])
    password = forms.CharField(max_length=32, min_length=6,
    error_messages={'required': '请输入密码','min_length':'密码至少为6位'})      # 密码
    repassword = forms.CharField(max_length=32, min_length=6,
    error_messages={'required': '请输入密码','min_length':'密码至少为6位'})  # 重新输入的密码

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username):
            raise ValidationError('用户名已存在')
        return username

    def clean_repassword(self):
        password =  self.cleaned_data.get("password")
        repassword =  self.cleaned_data.get("repassword")
        if (password != repassword):
            raise ValidationError('密码不一致，重新输入')
        return password

class booknoteform(forms.ModelForm):
    class Meta:
        model = Artical
        fields = "__all__"
        error_messages = {
           "bookname": {'required':'不能为空'},
           "content": {'required':'不能为空'},
         },

class Emailform(forms.Form):
    email = forms.CharField(max_length=32)
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email):
            raise ValidationError('邮箱已被使用')
        return email
