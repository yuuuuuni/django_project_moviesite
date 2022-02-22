from django.contrib import admin
from django.urls import path, include
from movie.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movie.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'), # '/'에 해당되는(가장 기본 url 페이지) path
]
