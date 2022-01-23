from django.contrib import admin

# Register your models here.
from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']


admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer, AnswerAdmin)
