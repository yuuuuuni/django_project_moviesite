from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자 속성 추가
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시 속성 추가


    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 외래키
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자 속성 추가
    modify_date = models.DateTimeField(null=True, blank=True) # 수정 일시 속성 추가


    def __str__(self):
        return self.content