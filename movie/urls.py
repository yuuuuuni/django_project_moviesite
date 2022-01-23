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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)