from django.shortcuts import render
import cv2

# Create your views here.

def room(request, room_name):
    print("wah")
    if request.method == "POST":
        newfile = cv2.imread("끄투.JPG")
        cv2.imwrite("test.jpg", newfile)
    return render(request, 'room.html', {
        'room_name': room_name
    })
