from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete' ),
    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'), # 질문의 댓글 등록 시에는 질문의 id번호가 필요
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'), # 질문의 댓글 수정 시에는 댓글의 id번호가 필요
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'), # 질문의 댓글 삭제 시에는 댓글의 id번호가 필요
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'), # 답변의 댓글 등록 시에는 답변의 id번호가 필요
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'), # 답변의 댓글 수정 시에는 댓글의 id번호가 필요
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'), # 답변의 댓글 삭제 시에는 댓글의 id번호가 필요

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)