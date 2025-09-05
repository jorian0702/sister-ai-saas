"""
Core URLs
コア機能のURL設定
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/', views.chat_page, name='chat'),
    path('code-review/', views.code_review_page, name='code_review'),
    path('api/status/', views.api_status, name='api_status'),
]