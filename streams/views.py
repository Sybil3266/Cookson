from django.shortcuts import render

import cv2
import threading, time
from streams import kcnn, utill
from collections import deque
import gzip
import numpy as np
from datetime import datetime
from django.http import StreamingHttpResponse


def makeimg(img):
    img = img[0:720, 170:1100]
    image = cv2.resize(img, (256, 256))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    return image


def show_mess(label):
    if label == 0 :
        print('라면 요리가 시작되었습니다, 물이 끓을때 까지 기다려주세요.')
    elif label == 1 :
        print('물이 끓기 시작합니다. 라면의 면을 넣어주세요.')
    elif label == 2 :
        print('면이 들어간 물이 끓을때 까지 기다려주세요.')
    elif label == 3 :
        print('물이 끓습니다. 라면의 면을 저어서 풀어주세요.')
    elif label == 4 :
        print('다음으로 라면의 분말스프를 안에 뿔려주세요.')
    elif label == 5 :
        print('분말스프가 뿌려진 면을 저어주세요.')
    elif label == 6 :
        print('스프가 고르게 퍼졌습니다. 다음으로 계란을 넣어주세요.')
    elif label == 7 :
        print('계란을 젓가락으로 저어주어 잘익게 해주세요.')
    elif label == 8 :
        print('계란이 어느정도 익었습니다. 면위에 파를 넣어주세요.')
    elif label == 9 :
        print('이제 약 10초간 더끓이신뒤 맛있는 라면을 드시면됩니다.')


exit_signal = threading.Event()


class VideoCamera(object):
    def __init__(self):
        self.prelabel = -1
        self.labQ = deque(maxlen=5)
        self.video = cv2.VideoCapture('r4.mp4')
        self.cnn = kcnn.kconvuph(10, 3)
        self.cnn.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
        self.cnn.load_weights('./cnnmodel/uphrcnn12cp')
        (self.grabbed, self.frame) = self.video.read()

        threading.daemon = True
        self.updater = threading.Thread(target=self.update, args=())
        self.updater.start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        #count = 0
        try :
            while (not exit_signal.is_set()) & (self.video.isOpened()):
                #count = count + 1
                #print (count)
                #time.sleep(0.1)
                for i in range(60):
                    (self.grabbed, self.frame) = self.video.read()
                    k = cv2.waitKey(1) & 0xff

                if k == ord('q'):
                    break

                #if count == 100 :
                #    exit_signal.set()

                if self.grabbed:
                    self.predict(self.cnn, self.frame)
                    self.prelabel = self.isnext_step(self.prelabel)
                else:
                    break
                #time.sleep(0.1)
        except :  # This is bad! replace it with proper handling
            exit_signal.set()
            print("child dead")

    def predict(self, cnn, img):
        img = np.asarray([makeimg(img)])
        n = datetime.now()
        predic = cnn.predict_on_batch(img)
        predic = np.argmax(predic, axis=1)
        self.labQ.extend(predic)

    def isnext_step(self, prelabel):
        if self.labQ.count(prelabel + 1) > 3:
            prelabel += 1
        return prelabel

    def get_step(self):
        return self.prelabel



def gen(cam):
    try:

        oldlabel = -5

        while not exit_signal.is_set():
            frame = cam.get_frame()
            label = cam.get_step()
            #show_mess(label)
            if oldlabel != label:
                show_mess(label)
            oldlabel = label

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            #time.sleep(0.1)

    except:  # This is bad! replace it with proper handling
        exit_signal.set()
        print("]CdC]")





#@gzip.gzip_page
def livefe(request, room_name):
    try:
        exit_signal.clear()
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        exit_signal.set()
        print("]CC]")

def index(request):
    return render(request, 'index.html', {})