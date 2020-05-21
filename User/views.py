from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def index(request):
    return render(request, 'index.html', {'user': request.session.get('user')})


def stream(request):
    return render(request, 'room.html', {'user': request.session.get('user')})


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
        self.request.session['user'] = form.data.get('username')
        return super().form_valid(form)


def Logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')

# def login(request):
#     if request.method == 'GET': 
#         return render(request, 'login.html')
#     elif request.method == 'POST':
#         username = request.session.get('Streamid-get', None)
#         password = request.session.get('Streampw-get', None)

#         res_data = {}
        
#     if not (username and password):
#         res_data['error'] = '입력오류 !'
#     else: 
#         user = User.objects.get(username = username)
#         if check_password(password, user.password):
#             request.session['user'] = user.username
#             return redirect('/')
#         else:
#             res_data['error'] = "비밀번호 오류"

#     return render(request, "login.html", res_data)


# def register(request):
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     elif request.method == 'POST':
#         username = request.POST.get('Registerid', None)
#         password = request.POST.get('Registerpw', None)
#         checkpassword = request.POST.get('Registerpw-confirm', None)
#         res_data = {}
#         if not (username and password and checkpassword):
#             res_data['error'] = '입력오류 !!'
#         elif password != checkpassword:
#             res_data['error'] = '비밀번호 불일치'
#         else:
#             if User.objects.get(username=username):
#                 res_data['error'] = '아이디 중복'
#             else:
#                 user = User(
#                     username=username,
#                     password=make_password(password),
#                 )
#                 user.save()
#                 return render(request, 'index.html')

#         return render(request, 'register.html', res_data)

