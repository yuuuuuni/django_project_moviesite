from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from movie.forms import QuestionForm
from movie.models import Question


@login_required(login_url='common:login')
def question_create(request): # 여기서의 request는 사용자가 subject와 content 창에 적은 내용이 넘어온 것
    """
    질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # author 속성에 로그인 계정 저장. request.user는 현재 로그인한 계정의 User 모델 객체
            question.create_date = timezone.now()
            question.save()
            return redirect('movie:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'movie/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id): # 질문 수정은 수정할 질문의 id가 필요하므로 question_id를 받음
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 로그인한 사용자와 질문한 작성자가 다르면
        messages.error(request, '수정 권한이 없습니다.') # 에러 메세지 모듈을 발생시켜라
        return redirect('movie:detail', question_id=question.id)

    if request.method == 'POST': # 값이 POST로 들어오면
        form = QuestionForm(request.POST, instance=question) # 기존 내용(instance=question)을 기준으로 보여주지만 수정된 내용(request.POST)이 있으면 그 request.POST의 값으로 덮은 후 QuestionForm을 form 변수에 넣어라
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save() # question은 그냥 사용자가 수정한 값을 담은 변수일뿐!
            return redirect('movie:detail', question_id=question.id) # 사용자가 입력한 값(수정한 값)을 담은 그 변수(question)의 번호(id)를 question_id에 지정해라
    else:
        form = QuestionForm(instance=question) # get방식이면 기존 내용이 채워져있는 QuestionForm을 form 변수에 대입해라
    context = {'form': form}
    return render(request, 'movie/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id) # question_id를 받아 Question객체(model에서 정의된)들 중 pk가 question_id인 것이 있으면 가져오고 그렇지 않으면 404 에러를 발생시켜라. 그것을 question라는 변수에 담음
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('movie:detail', question_id=question.id)
    else:
        question.delete()
    return redirect('movie:index')