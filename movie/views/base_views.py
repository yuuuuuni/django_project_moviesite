from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from movie.models import Question


def index(request):
    """
    질문 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지값. 페이지값이 따로 안정해지면 디폴트로 1 설정 만약 4페이지를 요청하면 page에 4가 들어감

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 5) # 페이지당 5개씩 보여주기
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