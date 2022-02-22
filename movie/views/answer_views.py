from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from movie.forms import AnswerForm
from movie.models import Question, Answer


@login_required(login_url='common:login')  # 로그인한 경우만 실행이 가능하도록 걸어두기
def answer_create(request, question_id):  # request에는 사용자가 적은 답변 내용이 넘어옴
    """
    답변 등록
    """
    question = get_object_or_404(Question,
                                 pk=question_id)  # question_id를 받아 Question객체들 중 pk값이 question_id인 것이 있으면 가져오고 그렇지 않으면 404 에러를 발생시켜라
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('movie:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'movie/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:  # 로그인한 사용자와 답변을 작성한 작성자가 다르면
        messages.error(request, '수정 권한이 없습니다.')  # 에러 메세지 모듈을 발생시켜라
        return redirect('movie:detail', question_id=answer.question.id)

    if request.method == 'POST':  # 값이 POST로 들어오면
        form = AnswerForm(request.POST,
                          instance=answer)  # 기존 내용(instance=answer)을 기준으로 보여주지만 수정된 내용(request.POST)이 있으면 그 request.POST의 값으로 덮은 후 AnswerForm을 form 변수에 넣어라
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()  # 수정일시 저장
            answer.save()  # answer는 그냥 사용자가 수정한 값을 담은 변수일뿐!
            return redirect('movie:detail',
                            question_id=answer.question.id)  # 사용자가 입력한 값(수정한 값)을 담은 그 변수(question)의 번호(id)를 question_id에 지정해라
    else:
        form = AnswerForm(instance=answer)  # get방식이면 기존 내용이 채워져있는 AnswerForm을 form 변수에 대입해라
    context = {'answer': answer, 'form': form}
    return render(request, 'movie/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer,
                               pk=answer_id)  # answer_id를 받아와서 Answer객체들 중(모델에 정의된) pk가 answer_id인 것이 있으면 보여주거나 없으면 404 오류를 보여줘라. 그것을 answer라는 변수에 담음
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('movie:detail', question_id=answer.question.id)
