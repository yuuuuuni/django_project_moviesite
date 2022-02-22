from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer


@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
    질문 추천 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author: # 로그인한 사용자와 질문의 작성자가 같으면
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else: # 로그인한 사용자와 질문의 작성자가 다르면
        question.voter.add(request.user) # Question 모델의 voter는 여러사람을 추가할 수 있는 ManyToManyField이므로 add 함수를 사용하여 추천인을 추가해야함
    return redirect('movie:detail', question_id=question.id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    답변 추천 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author: # 로그인한 사용자와 답변의 작성자가 같으면
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else: # 로그인한 사용자와 답변의 작성자가 다르면
        answer.voter.add(request.user)
    return redirect('movie:detail', question_id=answer.question.id)