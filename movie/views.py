from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone

from .forms import QuestionForm, AnswerForm, CommentForm
from .models import Question, Answer, Comment


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


@login_required(login_url='common:login') # 로그인한 경우만 실행이 가능하도록 걸어두기
def answer_create(request, question_id):  # request에는 사용자가 적은 답변 내용이 넘어옴
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk=question_id) # question_id를 받아 Question객체들 중 pk값이 question_id인 것이 있으면 가져오고 그렇지 않으면 404 에러를 발생시켜라
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


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author: # 로그인한 사용자와 답변을 작성한 작성자가 다르면
        messages.error(request, '수정 권한이 없습니다.') # 에러 메세지 모듈을 발생시켜라
        return redirect('movie:detail', question_id=answer.question.id)

    if request.method == 'POST': # 값이 POST로 들어오면
        form = AnswerForm(request.POST, instance=answer) # 기존 내용(instance=answer)을 기준으로 보여주지만 수정된 내용(request.POST)이 있으면 그 request.POST의 값으로 덮은 후 AnswerForm을 form 변수에 넣어라
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now() # 수정일시 저장
            answer.save() # answer는 그냥 사용자가 수정한 값을 담은 변수일뿐!
            return redirect('movie:detail', question_id=answer.question.id) # 사용자가 입력한 값(수정한 값)을 담은 그 변수(question)의 번호(id)를 question_id에 지정해라
    else:
        form = AnswerForm(instance=answer) # get방식이면 기존 내용이 채워져있는 AnswerForm을 form 변수에 대입해라
    context = {'answer': answer, 'form': form}
    return render(request, 'movie/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id) # answer_id를 받아와서 Answer객체들 중(모델에 정의된) pk가 answer_id인 것이 있으면 보여주거나 없으면 404 오류를 보여줘라. 그것을 answer라는 변수에 담음
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('movie:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    질문댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # 작성된 댓글 내용부터 임시저장
            comment.author = request.user # 로그인한 사용자를 댓글 글쓴이로 대입
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('movie:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    질문댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id) # comment_id를 받아 Comment객체(model에서 정의된)들 중 pk가 comment_id인 것이 있으면 가져오고 그렇지 않으면 404 에러를 발생시켜라. 그것을 comment라는 변수에 담음
    if request.user != comment.author:
        messages.error(request, '댓글 수정 권한이 없습니다.')
        return redirect('movie:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('movie:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    질문댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('movie:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('movie:detail', question_id=comment.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    답변댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('movie:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    답변댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id) # comment_id를 받아 Comment객체(model에서 정의된)들 중 pk가 comment_id인 것이 있으면 가져오고 그렇지 않으면 404 에러를 발생시켜라. 그것을 comment라는 변수에 담음
    if request.user != comment.author:
        messages.error(request, '댓글 수정 권한이 없습니다.')
        return redirect('movie:detail', question_id=comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('movie:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    답변댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('movie:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('movie:detail', question_id=comment.answer.question.id)