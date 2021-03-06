from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import cv2
import numpy
from .__init__ import cnn, labQ, prelabel
import threading
# Create your views here.


def index(request):
    return render(request, 'index.html')

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
    if request.method == "POST":
        reqimg = request.FILES["profile"].read()
        img = cv2.imdecode(numpy.fromstring(reqimg, numpy.uint8), cv2.IMREAD_UNCHANGED)
        # ret, jpeg = cv2.imencode('.jpg', img)

        npimg = numpy.asarray([makeimg(img)])
        predic = cnn.predict_on_batch(npimg)
        predic = numpy.argmax(predic, axis=1)
        labQ.extend(predic)
        if labQ.count((prelabel[0]) + 1) > 2:
            prelabel.popleft()
            next_movement = show_mess(prelabel[0])
            send_channel_message('chat_%s' % room_name, next_movement)

    return render(request, 'room.html', {'room_name': room_name})


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
