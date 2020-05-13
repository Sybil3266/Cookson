from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def index(request):
    return render(request, 'index.html', {'username': request.session.get('user')})


def login(request):
    if request.method == 'GET': 
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.session.get('Streamid-get', None)
        password = request.session.get('Streampw-get', None)

        res_data = {}
        
    if not (username and password):
        res_data['error'] = '입력오류'
    else: 
        user = User.objects.get(username = username)
        if check_password(password, user.password):
            request.session['user'] = user.username
            return redirect('/')
        else:
            res_data['error'] = "비밀번호 오류"

    return render(request, "login.html", res_data)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        checkpassword = request.POST.get('checkpassword', None)

        res_data = {}
        if not (username and password and checkpassword):
            res_data['error'] = '입력오류'
        elif password != checkpassword:
            res_data['error'] = '비밀번호 불일치'
        else:
            if User.objects.get(username=username):
                res_data['error'] = '아이디 중복'
            else:
                user = User(
                    username=username,
                    password=make_password(password),
                )
                user.save()

        return render(request, 'register.html', res_data)


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')
