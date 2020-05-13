import tensorflow as tf
from tensorflow import keras
import numpy as np
import pathlib as pl
import cv2
from streams import utill


#일반적인 cnn 모델 input:(128,128,3)
class Kconv(tf.keras.Model):

    def __init__(self,n_class,channel):
        super(Kconv, self).__init__(name='')

        self.conv1 = tf.keras.layers.Conv2D(
            8, (5, 5), padding='same',activation='relu', input_shape=(-1, 128, 128, channel))
        # conv = tf.nn.relu(conv)
        self.pool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.conv2 = tf.keras.layers.Conv2D(
            16, (3, 3), padding='same',activation='relu')

        self.pool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))
        self.drop = tf.keras.layers.Dropout(0.2)
        self.flat = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(64, 'relu')
        self.dense2 = tf.keras.layers.Dense(64, 'relu')
        self.dense3 = tf.keras.layers.Dense(64, 'relu')
        self.densesoft = tf.keras.layers.Dense(n_class, 'softmax')

    def call(self, imset, training=False):
        x = self.conv1(imset)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.drop(x)
        x = self.flat(x)
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.densesoft(x)
        return x


#h채널 비중을 높힌 cnn 모델
class Kconvuph(tf.keras.Model):

    def __init__(self,n_class,channel):
        super(Kconvuph, self).__init__(name='')

        self.hconv1 = tf.keras.layers.Conv2D(
            8, (5, 5), padding='same',activation='relu', input_shape=(-1, 128, 128, channel))
        # conv = tf.nn.relu(conv)
        self.hpool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.hconv2 = tf.keras.layers.Conv2D(
            32, (3, 3), padding='same',activation='relu')

        self.hpool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.sconv1 = tf.keras.layers.Conv2D(
            4, (5, 5), padding='same', activation='relu', input_shape=(-1, 128, 128, channel))
        # conv = tf.nn.relu(conv)
        self.spool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.sconv2 = tf.keras.layers.Conv2D(
            8, (3, 3), padding='same', activation='relu')

        self.spool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.vconv1 = tf.keras.layers.Conv2D(
            4, (5, 5), padding='same', activation='relu', input_shape=(-1, 128, 128, channel))
        # conv = tf.nn.relu(conv)
        self.vpool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.vconv2 = tf.keras.layers.Conv2D(
            8, (3, 3), padding='same', activation='relu')

        self.vpool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))

        self.drop = tf.keras.layers.Dropout(0.2)

        self.flat = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(64, 'relu')
        self.dense2 = tf.keras.layers.Dense(64, 'relu')
        self.dense3 = tf.keras.layers.Dense(64, 'relu')
        self.densesoft = tf.keras.layers.Dense(n_class, 'softmax')

    def call(self, imset, training=False):
        print(imset)

        #h,s,v 채널 나누기
        h = tf.unstack(imset, axis=3)[0]
        h = tf.reshape(h,(-1,128,128,1))
        s = tf.unstack(imset, axis=3)[1]
        s = tf.reshape(s, (-1, 128, 128, 1))
        v = tf.unstack(imset, axis=3)[2]
        v = tf.reshape(v, (-1, 128, 128, 1))
        print(h)

        h = self.hconv1(h)
        h = self.hpool1(h)
        h = self.hconv2(h)
        h = self.hpool2(h)

        s = self.sconv1(s)
        s = self.spool1(s)
        s = self.sconv2(s)
        s = self.spool2(s)

        v = self.vconv1(v)
        v = self.vpool1(v)
        v = self.vconv2(v)
        v = self.vpool2(v)

        h = self.drop(h)
        s = self.drop(s)
        v = self.drop(v)

        x = tf.concat((h,s,v),axis=3)
        #print(x)
        x = self.flat(x)
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.densesoft(x)
        return x

#오늘 추가한거 위에 모델이랑 같음
def kconvuph(n_class,channel):

    hsv = keras.Input(shape = (128,128,channel))

    h = tf.unstack(hsv, axis=3)[0]
    h = tf.reshape(h, (-1, 128, 128, 1))
    s = tf.unstack(hsv, axis=3)[1]
    s = tf.reshape(s, (-1, 128, 128, 1))
    v = tf.unstack(hsv, axis=3)[2]
    v = tf.reshape(v, (-1, 128, 128, 1))

    hconv1 = tf.keras.layers.Conv2D(
        8, (5, 5), padding='same',activation='relu', input_shape=(-1, 128, 128, channel))(h)
    # conv = tf.nn.relu(conv)
    hpool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(hconv1)

    hconv2 = tf.keras.layers.Conv2D(
        32, (3, 3), padding='same',activation='relu')(hpool1)

    hpool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(hconv2)

    sconv1 = tf.keras.layers.Conv2D(
        4, (5, 5), padding='same', activation='relu', input_shape=(-1, 128, 128, channel))(s)
    # conv = tf.nn.relu(conv)
    spool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(sconv1)

    sconv2 = tf.keras.layers.Conv2D(
        8, (3, 3), padding='same', activation='relu')(spool1)

    spool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(sconv2)

    vconv1 = tf.keras.layers.Conv2D(
        4, (5, 5), padding='same', activation='relu', input_shape=(-1, 128, 128, channel))(v)
    # conv = tf.nn.relu(conv)
    vpool1 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(vconv1)

    vconv2 = tf.keras.layers.Conv2D(
        8, (3, 3), padding='same', activation='relu')(vpool1)

    vpool2 = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(vconv2)

    x = tf.concat((hpool2, spool2, vpool2), axis=3)

    flat = tf.keras.layers.Flatten()(x)
    bn = keras.layers.BatchNormalization()(flat)

    d1 = tf.keras.layers.Dense(128, 'relu')(bn)
    d2 = tf.keras.layers.Dense(128, 'relu')(d1)
    d3 = tf.keras.layers.Dense(128, 'relu')(d2)
    drop = tf.keras.layers.Dropout(0.3)(d3)

    densesoft = tf.keras.layers.Dense(n_class, 'softmax')(drop)

    model = keras.Model(hsv,densesoft)

    return model

def set_hsv(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (h, w) = image.shape[:2]

    image = cv2.resize(image,(128,128))
    image = image / 255.0
    return image

def sub_train():
    root = './r1/'

    cnn = Kconv(10)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    imset = np.load(root + 'feature_np.npy')
    lset = np.load(root + 'label_np.npy')

    print(imset.shape)
    print(lset.shape)
    cnn.fit(imset, lset, 200, 6)
    cnn.save_weights('./cnnmodel/scnn6cp')

def train(ep):
    cnn = Kconv(10,3)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics= ['accuracy'])

    data_root = './r/'
    data_root = pl.Path(data_root)
    #하위 */*
    label_paths = list(data_root.glob('*'))
    imset = []
    lset = []
    for lp in label_paths:
        if str(lp)[-1:] != 'a':

            ips = list(lp.glob('*'))
            for ip in ips:
                imset.append(set_hsv(str(ip)))
                lset.append(int(str(lp)[-2:]))

    imset = np.asarray(imset)
    lset = np.asarray(lset)

    print(imset.shape)
    print(lset.shape)
    cnn.fit(imset,lset,200,ep)
    cnn.save_weights('./cnnmodel/cnn'+ep+'cp')

def rotate_train(ep):
    cnn = Kconv(10,3)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics= ['accuracy'])

    data_root = './r/'
    data_root = pl.Path(data_root)
    #하위 */*
    label_paths = list(data_root.glob('*'))
    imset = []
    lset = []
    for lp in label_paths:
        if str(lp)[-1:] != 'a':

            ips = list(lp.glob('*'))
            for ip in ips:
                r1,r2,r3,r4 = utill.rotate(utill.set_hsv(str(ip)))
                imset.append(r1)
                imset.append(r2)
                imset.append(r3)
                imset.append(r4)
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))

    lset = np.asarray(lset)
    imset = np.asarray(imset)

    print(imset.shape)
    print(lset.shape)
    cnn.fit(imset,lset,200,ep)
    cnn.save_weights('./cnnmodel/rcnn'+str(ep)+'cp')

def h_train(ep):
    cnn = Kconv(10,1)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics= ['accuracy'])

    data_root = './r/'
    data_root = pl.Path(data_root)
    #하위 */*
    label_paths = list(data_root.glob('*'))
    imset = []
    lset = []
    for lp in label_paths:
        if str(lp)[-1:] != 'a':

            ips = list(lp.glob('*'))
            for ip in ips:
                r1,r2,r3,r4 = utill.rotate(utill.set_h(str(ip)))
                imset.append(r1)
                imset.append(r2)
                imset.append(r3)
                imset.append(r4)
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))

    lset = np.asarray(lset)
    imset = np.asarray(imset)
    imset = imset.reshape((-1,128,128,1))
    print(imset.shape)
    print(lset.shape)
    cnn.fit(imset,lset,200,ep)
    cnn.save_weights('./cnnmodel/hrcnn'+str(ep)+'cp')


#이거 먼저 돌려줘서 훈련 시켜야함 로테이션 hsv 콜벡 추가
def uph_rotate_train(ep):
    cnn = kconvuph(10,3)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics= ['accuracy'])

    data_root = './r/'
    data_root = pl.Path(data_root)
    #하위 */*
    label_paths = list(data_root.glob('*'))
    imset = []
    lset = []
    for lp in label_paths:
        if str(lp)[-1:] != 'a':

            ips = list(lp.glob('*'))
            for ip in ips:
                r1,r2,r3,r4 = utill.rotate(utill.set_hsv(str(ip)))
                imset.append(r1)
                imset.append(r2)
                imset.append(r3)
                imset.append(r4)
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))
                lset.append(int(str(lp)[-2:]))

    lset = np.asarray(lset)
    imset = np.asarray(imset)

    print(imset.shape)
    print(lset.shape)

    es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=1,
                                                   mode='auto', restore_best_weights=True)

    cnn.fit(imset,lset,200,ep, callbacks = [es_callback], validation_split= 0.05)
    cnn.save_weights('./cnnmodel/uphrcnn'+str(ep)+'cp')


#예측 테스트용
def predictest():
    cnn = Kconv(11)
    cnn.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics= ['accuracy'])

    cnn.load_weights('./cnnmodel/cnn15cp')

    #여러개 예측
    data_root = './r/'
    data_root = pl.Path(data_root)
    # 하위 */*
    label_paths = list(data_root.glob('*'))
    imset = []
    lset = []
    for lp in label_paths:
        if str(lp)[-1:] != 'a':

            ips = list(lp.glob('*'))
            for ip in ips:
                imset.append(set_hsv(str(ip)))
                lset.append(int(str(lp)[-2:]))

    imset = np.asarray(imset)
    predic = cnn.predict(imset,1)
    predic = np.argmax(predic,axis=1)
    print(predic)
    """

    #한개 예측
    img = set_hsv('./r0/00/r0_1.png')
    img = [img]
    img = np.asarray(img)
    print(img.shape)
    predic = cnn.predict_on_batch(img)
    print(predic)
    """
#sub_train()
#train()
#predictest()
#rotate_train(5)
#h_train()
#uph_rotate_train(12)