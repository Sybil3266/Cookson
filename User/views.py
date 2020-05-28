from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def index(request):
    return render(request, 'index.html')


def stream(request):
    return render(request, 'room.html')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            username=form.data.get('username'),
            password=make_password(form.data.get('password')),
        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):  # 로그인 가능여부 확인 후
        user = authenticate(
            username=form.data.get('username'),
            password=form.data.get('password')
        )

        if user is not None:
            login(self.request,user)
            self.request.session['user'] = user.username

        return super().form_valid(form)


def Logout(request):

    logout(request)
    return redirect('/')

