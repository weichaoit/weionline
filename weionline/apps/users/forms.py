# _*_ coding: utf-8 _*_
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    ''' 登陆表单验证'''
    # 用户名和密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    '''注册表单验证'''
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,max_length=20)
    # 验证码,可以自定义错误提示
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetForm(forms.Form):
    '''找回密码'''
    email = forms.EmailField(required=True)
    # 验证码,可以自定义错误提示
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ModifyPwdForm(forms.Form):
    ''' 登陆表单验证'''
    # 用户名和密码不能为空
    password = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)
