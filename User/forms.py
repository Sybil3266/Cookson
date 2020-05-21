from django import forms
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class RegisterForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User #Modelform에서 가져올 form, password의경우는 widget을 위해 field로 직접 받도록 함

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다!')

        return cd['confirm_password']


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        check_password = cleaned_data.get('check_password')

        if password and check_password:
            if password != check_password:
                self.add_error('password', '비밀번호가 일치하지 않습니다!')


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
        except (NameError, ObjectDoesNotExist):
            self.add_error('username', '아이디가 잘못된것 같아요!')
            return
        
        if not check_password(password, user.password):
            self.add_error('password', '비밀번호')
