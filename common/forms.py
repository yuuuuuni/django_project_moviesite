from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일") # 이메일 필드 추가

    class Meta:
        model = User # 사용할 모델 이름
        fields = ['username', 'password1', 'password2', 'email'] # UserForm에서 사용할 User 모델의 속성