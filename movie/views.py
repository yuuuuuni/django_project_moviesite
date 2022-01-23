from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question


def index(request):
    """
    질문 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'movie/question_list.html', context)


def detail(request, question_id):
    """
     질문 상세 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'movie/question_detail.html', context)


def answer_create(request, question_id):  # request에는 사용자가 적은 답변 내용이 넘어옴
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('movie:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'movie/question_detail.html', context)


def question_create(request): # 여기서의 request는 사용자가 subject와 content 창에 적은 내용이 넘어온 것
    """
    질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('movie:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'movie/question_form.html', context)