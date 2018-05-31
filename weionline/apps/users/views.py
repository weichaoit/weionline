from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from untils.email_send import send_register_eamil
# Create your views here.


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    return render(request,'index.html')


class CustomBackend(ModelBackend):
    '''
    邮箱和用户名都可以登录
    基础ModelBackend类，因为它有authenticate方法
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None


class LoginView(View):
    '''登陆视图'''
    def get(self,request):
        return render(request, 'user/login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        # 验证登陆字段是否正确
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 验证用户和密码
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 验证是否通过邮箱激活
                if user.is_active:
                    # 使用户登陆
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request,'user/login.html',{'msg':'请登录邮箱后激活您的账户'})
            else:
                return render(request,'user/login.html',{'msg':'用户名或者密码错误','login_form':login_form})
        else:
            return render(request, 'user/login.html',{'login_form':login_form})


class RegisterView(View):
    '''注册视图'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'user/register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user_name = request.POST.get('email','')

            # 查看该email是否被注册
            if UserProfile.objects.filter(email=user_name):
                return render(request,'user/register.html',{'register_form':register_form,'msg':'该账号已经被注册'})

            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'user/login.html')
        else:
            return render(request,'user/register.html',{'register_form':register_form})


class ActiveUserView(View):
    '''通过点击邮箱内的链接激活账户'''
    def get(self,request,code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'user/active_fail.html')

        return render(request,'user/login.html')


class ForgetView(View):
    '''
    忘记密码
    get 进入忘记密码页面
    post 发送邮件
    '''
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'user/forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_eamil(email,'forget')
            return render(request,'user/send_success.html')
        else:
            return render(request,'user/forgetpwd.html',{'forget_form':forget_form})


class ResetView(View):
    '''显示修改密码页视图'''
    def get(self,request,code):
        # 通过code 查询出用户的email
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'user/password_reset.html',{'email':email})
        else:
            return render(request,'user/active_fail.html')

        return render(request,'user/login.html')


class ModifyPwd(View):
    '''修改密码'''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd = request.POST.get('password','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd != pwd2:
                # 密码不一致后的操作
                return render(request,'user/password_reset.html',{
                    'email':email,
                    'msg':'两次密码输入不一致'
                })

            # 修改数据
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd)
            user.save()

            return render(request,'user/login.html')
        else:
            email = request.POST.get('email','')
            return render(request,'user/password_reset.html',{'email':email,'modify_form':modify_form})







