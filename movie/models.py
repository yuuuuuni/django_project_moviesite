from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model): # 질문 모델
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')  # 질문의 작성자
    subject = models.CharField(max_length=200)  # 질문 제목
    content = models.TextField()  # 질문 내용
    create_date = models.DateTimeField()  # 질문 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)  # 질문 수정일시
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인

    def __str__(self):
        return self.subject


class Answer(models.Model): # 답변 모델
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')  # 작성자 속성 추가
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 외래키, 답변의 연결된 질문
    content = models.TextField()  # 답변 내용
    create_date = models.DateTimeField()  # 답변 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)  # 답변 수정일시
    voter = models.ManyToManyField(User, related_name='voter_answer') # 추천인

    def __str__(self):
        return self.content


class Comment(models.Model): # 댓글 모델
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 작성자
    content = models.TextField() # 댓글 내용
    create_date = models.DateTimeField() # 댓글 작성일시
    modify_date = models.DateTimeField(null=True, blank=True) # 댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 답변