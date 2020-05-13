
import numpy as np
import cv2
import random
import pathlib as pl



#image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
def set_hsv(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (h, w) = image.shape[:2]

    image = cv2.resize(image,(128,128))
    image = image / 255.0
    return image

def set_h(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (h, w) = image.shape[:2]

    image = cv2.resize(image,(128,128))
    h_img = np.split(image,3,axis = 2)[0]
    h_img = np.reshape(h_img,(128,128))
    image = h_img / 255.0
    return image


def img_cut(image):

    (h, w) = image.shape[:2]


    point_img = []

    point_img.append(image[0:int(h/10), int(w/10*5): int(w/10*6)])

    point_img.append(image[int(h/10*1):int(h/10*2), int(w/10*3): int(w/10*4)])
    point_img.append(image[int(h/10*1):int(h/10*2), int(w/10*5): int(w/10*6)])
    point_img.append(image[int(h/10*1):int(h/10*2), int(w/10*7): int(w/10*8)])

    point_img.append(image[int(h/10*3):int(h/10*4), int(w/10*2): int(w/10*3)])
    point_img.append(image[int(h/10*3):int(h/10*4), int(w/10*4): int(w/10*5)])
    point_img.append(image[int(h/10*3):int(h/10*4), int(w/10*6): int(w/10*7)])
    point_img.append(image[int(h/10*3):int(h/10*4), int(w/10*8): int(w/10*9)])

    point_img.append(image[int(h/10*5):int(h/10*6), int(w/10*2): int(w/10*3)])
    point_img.append(image[int(h/10*5):int(h/10*6), int(w/10*4): int(w/10*5)])
    point_img.append(image[int(h/10*5):int(h/10*6), int(w/10*5): int(w/10*6)])
    point_img.append(image[int(h/10*5):int(h/10*6), int(w/10*6): int(w/10*7)])
    point_img.append(image[int(h/10*5):int(h/10*6), int(w/10*8): int(w/10*9)])

    point_img.append(image[int(h/10*7):int(h/10*8), int(w/10*2): int(w/10*3)])
    point_img.append(image[int(h/10*7):int(h/10*8), int(w/10*4): int(w/10*5)])
    point_img.append(image[int(h/10*7):int(h/10*8), int(w/10*6): int(w/10*7)])
    point_img.append(image[int(h/10*7):int(h/10*8), int(w/10*8): int(w/10*9)])

    point_img.append(image[int(h/10*8):int(h/10*9), int(w/10*3): int(w/10*4)])
    point_img.append(image[int(h/10*8):int(h/10*9), int(w/10*5): int(w/10*6)])
    point_img.append(image[int(h/10*8):int(h/10*9), int(w/10*7): int(w/10*8)])

    point_img.append(image[int(h/10*9):int(h/10*10), int(w/10*5): int(w/10*6)])

    return point_img

def check_cnt(img,path):
    """

    #0
    img = img[0:720, 170:1100]
    image = cv2.resize(img,(256,256))
    cv2.imwrite(path, image)

    #1
    #img = img[0:720, 170:1030]
    image = cv2.resize(img,(256,256))
    cv2.imwrite(path, image)
    """
    # 2,3
    img = img[0:720, 170:1100]
    image = cv2.resize(img, (256, 256))
    cv2.imwrite(path, image)


def cnt_cut(imset,x1,x2,y1,y2):
    for image in imset:
        point_img = image[x1:x2 , y1:y2]

def show_cut(img):
    #0
    #cv2.line(img, (200, 0), (1100, 720), (0, 255, 0), 1)
    #1
    #cv2.line(img, (170, 0), (1070, 720), (0, 255, 0), 1)
    #2
    cv2.line(img, (170, 0), (1100, 720), (0, 255, 0), 1)

    cv2.imshow('ss',img)
    cv2.waitKey(50)

def test_sub():
    img1 = cv2.imread('./r1/00/r1_0.png')/255.0
    img2 = cv2.imread('./r1/01/r1_167.png')/255.0
    subimg = img2 - img1
    subimg = np.asarray(subimg)
    print(subimg.shape)
def make_sub():
    root = './r1/'
    data_root = pl.Path(root)
    # 하위 */*
    label_paths = list(data_root.glob('*'))
    aimset = []
    lset = []
    for lp in label_paths:

        if str(lp)[-1:] != 'a':
            imset = []
            ips = list(lp.glob('*'))
            for ip in ips:
                imset.append(set_hsv(str(ip)))
                lset.append(int(str(lp)[-2:]))
            aimset.append(imset)

    feature = []
    label = []
    for i in range(1,len(aimset)):


        pimset = aimset[i-1][:10]
        nimset = aimset[i]

        for pi in pimset:
            for ni in nimset:
                feature.append(pi - ni)
                label.append(i)

    for ims in aimset:
        pimset = ims[:10]
        nimset = ims

        for pi in pimset:
            for ni in nimset:
                feature.append(pi - ni)
                label.append(100)
    feature = np.asarray(feature)
    label = np.asarray(label)
    np.save(root + 'feature_np', feature)
    np.save(root + 'label_np', label)

def rotate(img):

    (h, w) = img.shape[:2]
    # calculate the center of the image
    center = (w / 2, h / 2)

    angle90 = 90
    angle180 = 180
    angle270 = 270

    scale = 1.0

    # Perform the counter clockwise rotation holding at the center
    # 90 degrees
    M = cv2.getRotationMatrix2D(center, angle90, scale)
    rotated90 = cv2.warpAffine(img, M, (h, w))

    # 180 degrees
    M = cv2.getRotationMatrix2D(center, angle180, scale)
    rotated180 = cv2.warpAffine(img, M, (w, h))

    # 270 degrees
    M = cv2.getRotationMatrix2D(center, angle270, scale)
    rotated270 = cv2.warpAffine(img, M, (h, w))

    return img, rotated90, rotated180, rotated270

