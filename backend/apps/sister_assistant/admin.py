"""
Sister Assistant Admin
紗良アシスタント機能の管理画面設定
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ChatSession, ChatMessage, CodeReview, ProjectSuggestion,
    SisterPersonalityConfig, UserInteraction, AIModelUsage
)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'is_active', 'message_count']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'メッセージ数'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_title', 'role', 'content_preview', 'timestamp', 'ai_model']
    list_filter = ['role', 'ai_model', 'timestamp']
    search_fields = ['content', 'session__title']
    readonly_fields = ['id', 'timestamp']
    
    def session_title(self, obj):
        return obj.session.title
    session_title.short_description = 'セッション'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'メッセージ内容'


@admin.register(CodeReview)
class CodeReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'status', 'created_at', 'tokens_used']
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['id', 'created_at', 'completed_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'title', 'language', 'status')
        }),
        ('コード', {
            'fields': ('original_code',),
            'classes': ('collapse',)
        }),
        ('レビュー結果', {
            'fields': ('review_result', 'suggestions'),
            'classes': ('collapse',)
        }),
        ('メタデータ', {
            'fields': ('created_at', 'completed_at', 'ai_model', 'tokens_used'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectSuggestion)
class ProjectSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'suggestion_type', 'priority', 'is_implemented', 'created_at']
    list_filter = ['suggestion_type', 'priority', 'is_implemented', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['id', 'created_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'title', 'description', 'suggestion_type', 'priority')
        }),
        ('提案内容', {
            'fields': ('current_situation', 'proposed_solution', 'expected_benefits', 'implementation_steps')
        }),
        ('実装状況', {
            'fields': ('is_implemented', 'implementation_date')
        }),
        ('メタデータ', {
            'fields': ('created_at', 'ai_confidence'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SisterPersonalityConfig)
class SisterPersonalityConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'custom_name', 'friendliness', 'technical_depth', 'updated_at']
    search_fields = ['user__username', 'custom_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本設定', {
            'fields': ('user', 'custom_name', 'custom_greeting', 'preferred_language')
        }),
        ('性格パラメータ', {
            'fields': ('friendliness', 'technical_depth', 'helpfulness', 'casualness'),
            'description': '各パラメータは0.0〜1.0の範囲で設定してください'
        }),
        ('学習設定', {
            'fields': ('learn_from_interactions', 'remember_preferences')
        }),
        ('メタデータ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'interaction_type', 'content_preview', 'user_rating', 'timestamp']
    list_filter = ['interaction_type', 'user_rating', 'timestamp']
    search_fields = ['user__username', 'content', 'response']
    readonly_fields = ['id', 'timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容'


@admin.register(AIModelUsage)
class AIModelUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'model_name', 'feature_used', 'total_tokens', 'cost_estimate', 'timestamp']
    list_filter = ['model_name', 'feature_used', 'timestamp']
    search_fields = ['user__username']
    readonly_fields = ['timestamp']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# カスタム管理画面の設定
admin.site.site_header = "Sister SaaS 管理画面"
admin.site.site_title = "Sister SaaS Admin"
admin.site.index_title = "紗良とお兄ちゃんの開発ごっこ管理"