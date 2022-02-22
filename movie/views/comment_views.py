from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from movie.forms import CommentForm
from movie.models import Question, Answer, Comment


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    질문 댓글 등록
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
            return redirect('{}#comment_{}'.format(resolve_url('movie:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    질문 댓글 수정
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
            return redirect('{}#comment_{}'.format(resolve_url('movie:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    질문 댓글 삭제
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
    답변 댓글 등록
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
            return redirect('{}#comment_{}'.format(resolve_url('movie:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    답변 댓글 수정
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
            return redirect('{}#comment_{}'.format(resolve_url('movie:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'movie/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    답변 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('movie:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('movie:detail', question_id=comment.answer.question.id)