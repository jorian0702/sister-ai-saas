"""
Sister Assistant Models
紗良アシスタント機能のデータベースモデル
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class ChatSession(models.Model):
    """チャットセッション"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, default='新しいチャット')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'チャットセッション'
        verbose_name_plural = 'チャットセッション'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ChatMessage(models.Model):
    """チャットメッセージ"""
    ROLE_CHOICES = [
        ('user', 'ユーザー'),
        ('assistant', 'アシスタント'),
        ('system', 'システム'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # AI関連フィールド
    ai_model = models.CharField(max_length=50, blank=True, null=True)
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(default=0.0)  # seconds
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'チャットメッセージ'
        verbose_name_plural = 'チャットメッセージ'
    
    def __str__(self):
        return f"{self.session.title} - {self.role}: {self.content[:50]}..."


class CodeReview(models.Model):
    """コードレビュー"""
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('typescript', 'TypeScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('other', 'その他'),
    ]
    
    REVIEW_STATUS = [
        ('pending', '処理中'),
        ('completed', '完了'),
        ('failed', '失敗'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_reviews')
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    original_code = models.TextField()
    review_result = models.TextField(blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='pending')
    
    # メタデータ
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    ai_model = models.CharField(max_length=50, blank=True)
    tokens_used = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'コードレビュー'
        verbose_name_plural = 'コードレビュー'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_completed(self):
        """レビュー完了をマーク"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class ProjectSuggestion(models.Model):
    """プロジェクト改善提案"""
    SUGGESTION_TYPE = [
        ('architecture', 'アーキテクチャ'),
        ('performance', 'パフォーマンス'),
        ('security', 'セキュリティ'),
        ('code_quality', 'コード品質'),
        ('testing', 'テスト'),
        ('deployment', 'デプロイメント'),
        ('other', 'その他'),
    ]
    
    PRIORITY_LEVEL = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('critical', '緊急'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_suggestions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    suggestion_type = models.CharField(max_length=20, choices=SUGGESTION_TYPE)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVEL, default='medium')
    
    # 提案内容
    current_situation = models.TextField(help_text='現在の状況')
    proposed_solution = models.TextField(help_text='提案する解決策')
    expected_benefits = models.TextField(help_text='期待される効果')
    implementation_steps = models.JSONField(default=list, help_text='実装手順')
    
    # メタデータ
    created_at = models.DateTimeField(auto_now_add=True)
    is_implemented = models.BooleanField(default=False)
    implementation_date = models.DateTimeField(null=True, blank=True)
    ai_confidence = models.FloatField(default=0.0, help_text='AI提案の信頼度(0-1)')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'プロジェクト提案'
        verbose_name_plural = 'プロジェクト提案'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SisterPersonalityConfig(models.Model):
    """紗良の性格設定"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sister_config')
    
    # 性格パラメータ
    friendliness = models.FloatField(default=0.8, help_text='親しみやすさ (0-1)')
    technical_depth = models.FloatField(default=0.7, help_text='技術的深度 (0-1)')
    helpfulness = models.FloatField(default=0.9, help_text='親切さ (0-1)')
    casualness = models.FloatField(default=0.6, help_text='カジュアルさ (0-1)')
    
    # カスタマイズ設定
    custom_name = models.CharField(max_length=50, default='紗良', help_text='アシスタントの名前')
    custom_greeting = models.TextField(blank=True, help_text='カスタム挨拶')
    preferred_language = models.CharField(max_length=10, default='ja', help_text='優先言語')
    
    # 学習設定
    learn_from_interactions = models.BooleanField(default=True)
    remember_preferences = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '紗良設定'
        verbose_name_plural = '紗良設定'
    
    def __str__(self):
        return f"{self.user.username}の紗良設定"


class UserInteraction(models.Model):
    """ユーザーインタラクション履歴"""
    INTERACTION_TYPE = [
        ('chat', 'チャット'),
        ('code_review', 'コードレビュー'),
        ('suggestion', '提案'),
        ('feedback', 'フィードバック'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE)
    content = models.TextField()
    response = models.TextField(blank=True)
    
    # 評価
    user_rating = models.IntegerField(null=True, blank=True, help_text='ユーザー評価 (1-5)')
    user_feedback = models.TextField(blank=True, help_text='ユーザーフィードバック')
    
    # メタデータ
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    context_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'ユーザーインタラクション'
        verbose_name_plural = 'ユーザーインタラクション'
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.timestamp}"


class AIModelUsage(models.Model):
    """AI モデル使用統計"""
    MODEL_CHOICES = [
        ('gpt-4', 'GPT-4'),
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
        ('claude-3-sonnet', 'Claude 3 Sonnet'),
        ('claude-3-haiku', 'Claude 3 Haiku'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_usage')
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES)
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # 使用コンテキスト
    feature_used = models.CharField(max_length=50)  # chat, code_review, suggestion
    session_id = models.CharField(max_length=100, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'AIモデル使用統計'
        verbose_name_plural = 'AIモデル使用統計'
    
    def __str__(self):
        return f"{self.user.username} - {self.model_name} - {self.timestamp}"
    
    @property
    def total_tokens(self):
        return self.tokens_input + self.tokens_output