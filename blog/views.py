import string
from io import BytesIO
import random
from random import randint

from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views import View

from blog.forms import LoginForm, RegisterForm
from blog.models import User, Person, Exponent
from mysite.settings import STATICFILES_DIRS


def set_session(request, username='', nickname='', page='index'):
    # 设置 session
    request.session['username'] = username
    request.session['nickname'] = nickname
    request.session['page'] = page


# 首页
def index(request):
    username = request.session.get('username', '')
    nickname = request.session.get('nickname', '')
    set_session(request, username, nickname)
    return render(request, 'blog/index.html')


# 登录页
class LoginView(View):
    def get(self, request):
        return render(request, 'blog/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # 设置 session
            username = form.cleaned_data.get('username')
            person = Person.objects.get(user__username=username)
            set_session(request, username=username, nickname=person.nickname)
            # 验证码验证
            check_code_input = form.cleaned_data.get('check_code')
            check_code = request.session.get('check_code')
            if check_code.lower() != check_code_input.lower():
                form.add_error('check_code', '验证码错误')
            else:
                return redirect(reverse('blog:index'))
        return render(request, 'blog/login.html', {'form': form})


# 注册页
class RegisterView(View):
    def get(self, request):
        return render(request, 'blog/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        # 表单验证通过则创建用户，否则返回页面并给出相应的提示
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            pwd = make_password(password)
            # 验证码验证
            check_code_input = form.cleaned_data.get('check_code')
            check_code = request.session.get('check_code')
            if check_code.lower() != check_code_input.lower():
                form.add_error('check_code', '验证码错误')
            else:
                # 创建用户数据
                user = User.objects.create(username=username, email=email, password=pwd, status=True, active=True)
                Person.objects.create(user=user, nickname=username)
                Exponent.objects.create(user=user)
                return redirect(reverse('blog:login'))
        return render(request, 'blog/register.html', {'form': form})


# 退出登录
def logout(request):
    # 将 session 恢复默认值
    set_session(request)
    return redirect(reverse('blog:index'))


# 验证码
def get_code(request):
    img = Image.new('RGB', (120, 60), (255, 255, 255))
    font = ImageFont.truetype(STATICFILES_DIRS[0] + '/blog/fonts/DroidSans.ttf', randint(25, 30))
    draw = ImageDraw.Draw(img)
    check_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # 元素点
    for _ in range(1000):
        draw.point((randint(0, 120), randint(0, 60)), (randint(0, 255), randint(0, 255), randint(0, 255)))
    # 验证码
    for i in range(6):
        draw.text((5 + i * 20, randint(5, 35)), check_code[i], (0, 0, 0), font)
    # 横线
    for x in range(0, 121):
        for y in range(15, 46, 15):
            draw.point((x, y), (0, 0, 0))

    fp = BytesIO()
    img.save(fp, 'png')
    request.session['check_code'] = check_code
    return HttpResponse(fp.getvalue(), content_type='image/png')
