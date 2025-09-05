"""
Core Views
メインページとコア機能のビュー
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from apps.sister_assistant.models import ChatSession, CodeReview, ProjectSuggestion
import json


def home(request):
    """ホームページ"""
    context = {
        'sister_name': '紗良',
        'user_name': request.user.username if request.user.is_authenticated else 'お兄ちゃん'
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """ダッシュボード"""
    user = request.user
    
    # ユーザーの統計情報を取得
    chat_sessions_count = ChatSession.objects.filter(user=user).count()
    code_reviews_count = CodeReview.objects.filter(user=user).count()
    suggestions_count = ProjectSuggestion.objects.filter(user=user).count()
    
    # 最新のアクティビティ
    recent_chats = ChatSession.objects.filter(user=user)[:5]
    recent_reviews = CodeReview.objects.filter(user=user)[:5]
    recent_suggestions = ProjectSuggestion.objects.filter(user=user)[:5]
    
    context = {
        'stats': {
            'chat_sessions': chat_sessions_count,
            'code_reviews': code_reviews_count,
            'suggestions': suggestions_count,
        },
        'recent_chats': recent_chats,
        'recent_reviews': recent_reviews,
        'recent_suggestions': recent_suggestions,
    }
    
    return render(request, 'core/dashboard.html', context)


def chat_page(request):
    """チャットページ"""
    return render(request, 'core/chat.html')


def code_review_page(request):
    """コードレビューページ"""
    return render(request, 'core/code_review.html')


@require_http_methods(["GET"])
def api_status(request):
    """API ステータス確認"""
    return JsonResponse({
        'status': 'ok',
        'sister_name': '紗良',
        'message': 'お兄ちゃん、システムは正常に動作してるよ！',
        'features': {
            'chat': True,
            'code_review': True,
            'suggestions': True,
            'real_time': True,
        }
    })