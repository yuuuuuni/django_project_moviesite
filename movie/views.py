from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question


def index(request):
    """
    질문 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지값. 페이지값이 따로 안정해지면 디폴트로 1 설정 만약 4페이지를 요청하면 page에 4가 들어감

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page) # (page)에 들어간 숫자에 해당하는 (10개씩 게시물을 보여주는)페이지를 꺼내서 page_obj 객체를 생성해라

    context = {'question_list': page_obj} # question_list는 페이징 객체(page_obj)
    return render(request, 'movie/question_list.html', context)


def detail(request, question_id):
    """
     질문 상세 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'movie/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):  # request에는 사용자가 적은 답변 내용이 넘어옴
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('movie:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'movie/question_detail.html', context)


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