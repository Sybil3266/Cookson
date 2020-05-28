from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import cv2
import numpy
from .__init__ import cnn, labQ, prelabel
# Create your views here.


def index(request):
    return render(request, 'index.html', {'user': request.session.get('user')})

def makeimg(img):
    img = img[0:720, 170:1100]
    image = cv2.resize(img, (256, 256))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    return image

def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'chat_message',
            'message': message
        }
    )

def show_mess(label):
    if label == 0 :
        return '라면 요리가 시작되었습니다, 물이 끓을때 까지 기다려주세요.'
    elif label == 1 :
        return '물이 끓기 시작합니다. 라면의 면을 넣어주세요.'
    elif label == 2 :
        return '면이 들어간 물이 끓을때 까지 기다려주세요.'
    elif label == 3 :
        return '물이 끓습니다. 라면의 면을 저어서 풀어주세요.'
    elif label == 4 :
        return '다음으로 라면의 분말스프를 안에 뿔려주세요.'
    elif label == 5 :
        return '분말스프가 뿌려진 면을 저어주세요.'
    elif label == 6 :
        return '스프가 고르게 퍼졌습니다. 다음으로 계란을 넣어주세요.'
    elif label == 7 :
        return '계란을 젓가락으로 저어주어 잘익게 해주세요.'
    elif label == 8 :
        return '계란이 어느정도 익었습니다. 면위에 파를 넣어주세요.'
    elif label == 9 :
        return '이제 약 10초간 더끓이신뒤 맛있는 라면을 드시면됩니다.'

def stream(request, room_name):
    print("wah")
    if request.method == "POST":
        profile = request.FILES["profile"].read()
        img = cv2.imdecode(numpy.fromstring(profile, numpy.uint8), cv2.IMREAD_UNCHANGED)
        #ret, jpeg = cv2.imencode('.jpg', img)

        npimg = numpy.asarray([makeimg(img)])
        predic = cnn.predict_on_batch(npimg)
        predic = numpy.argmax(predic, axis=1)
        labQ.extend(predic)
        if labQ.count((prelabel[0]) + 1) > 0:
            prelabel.popleft()
            next_movement = show_mess(prelabel[0])
            send_channel_message('chat_%s' % room_name, next_movement)

        cv2.imwrite(room_name + '.jpg', img)

    return render(request, 'room.html', {'user': request.session.get('user'), 'room_name': room_name})


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

