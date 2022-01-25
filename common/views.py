from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.forms import UserForm


def signup(request): # 사용자가 입력한 회원가입 내용
    """
    계정 생성
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 사용자 인증. username, password가 값이 다 맞으면 user에 넣어라
            login(request, user) # 로그인해라
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})