from getpass import getuser
from multiprocessing.util import is_exiting

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
import requests

# def user_register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form_data = {
#                 'email' : request.POST['username'],
#                 'password' : request.POST['password'],
#                 }
#
#
#             # user = form.save(commit=False)
#             # user.set_password(form.cleaned_data['password'])  # Хешируем пароль
#             # user.save()
#             messages.success(request, "Вы успешно зарегистрированы!")
#             return redirect("login")
#     else:
#         form = RegisterForm()
#
#     return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        # form = LoginForm(data=request.POST)
        # if form.is_valid():
        form_data = {
            'email': request.POST['username'],
            'password': request.POST['password'],
        }
        res = requests.post('https://api.myedu.oshsu.kg/public/api/login', form_data)
        if res.status_code == 200:
            token = res.json()['authorisation']['token']
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",  # Указываем тип контента, если нужно
            }
            userinfo = requests.get('https://api.myedu.oshsu.kg/public/api/user',headers=headers)
            getuser = userinfo.json()['user']
            email = getuser['email']
            password = request.POST['password']
            username =  getuser['last_name'] + ' ' + getuser['name']
            # print(getuser['email'])
            is_exists = User.objects.filter(email=email).exists()

            if not is_exists :
                user = User.objects.create(
                    email = email,
                    username = username,
                    password = password
                )
                user.set_password(password)
                user.save()
            else:
                user = User.objects.get(email=email)
            # user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect("schedule")  # Перенаправляем на главную

    form = LoginForm()
    request.session.set_expiry(3600)  #
    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect("login")
