"""
Sister SaaS URL Configuration
お兄ちゃんと紗良の開発ごっこプロジェクトのURL設定
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include('apps.ai_chat.urls')),
    path('api/v1/', include('apps.sister_assistant.urls')),
    path('api/v1/', include('apps.user_management.urls')),
    
    # Core app (メインページ)
    path('', include('apps.core.urls')),
]

# Development時の静的ファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Admin site customization
admin.site.site_header = "Sister SaaS 管理画面"
admin.site.site_title = "Sister SaaS"
admin.site.index_title = "お兄ちゃんと紗良の開発ごっこ管理"