from django.urls import path

from .views import LoginView, RegisterView, Logout, stream

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', Logout),
    path('<str:room_name>/', stream, name='room'),
]
