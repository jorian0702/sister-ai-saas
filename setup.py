#!/usr/bin/env python3
"""
Sister SaaS Setup Script
お兄ちゃんと紗良の開発ごっこプロジェクト セットアップスクリプト
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, check=True):
    """コマンドを実行する"""
    print(f"実行中: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"エラー: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def check_python_version():
    """Python バージョンをチェック"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11 以上が必要です")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """必要な依存関係をチェック"""
    dependencies = ['git', 'docker', 'docker-compose']
    missing = []
    
    for dep in dependencies:
        if not shutil.which(dep):
            missing.append(dep)
        else:
            print(f"✅ {dep} が見つかりました")
    
    if missing:
        print(f"❌ 以下のツールが見つかりません: {', '.join(missing)}")
        print("これらのツールをインストールしてから再実行してください。")
        return False
    
    return True


def create_virtual_environment():
    """仮想環境を作成"""
    print("\n📦 仮想環境を作成中...")
    if os.path.exists('venv'):
        print("仮想環境が既に存在します。")
        return True
    
    return run_command(f"{sys.executable} -m venv venv")


def install_requirements():
    """依存関係をインストール"""
    print("\n📦 依存関係をインストール中...")
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
    
    return run_command(f"{pip_path} install -r backend/requirements.txt")


def setup_environment():
    """環境変数ファイルをセットアップ"""
    print("\n⚙️  環境設定をセットアップ中...")
    
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✅ .env ファイルを作成しました")
        print("⚠️  .env ファイルを編集してAPIキーなどを設定してください")
    else:
        print(".env ファイルが既に存在します")
    
    return True


def setup_database():
    """データベースをセットアップ"""
    print("\n🗄️  データベースをセットアップ中...")
    
    os.chdir('backend')
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        python_path = "..\\venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_path = "../venv/bin/python"
    
    success = True
    success &= run_command(f"{python_path} manage.py migrate")
    success &= run_command(f"{python_path} manage.py collectstatic --noinput")
    
    # Create superuser (optional)
    print("\n👤 管理者ユーザーを作成しますか？ (y/n): ", end="")
    if input().lower() == 'y':
        run_command(f"{python_path} manage.py createsuperuser", check=False)
    
    os.chdir('..')
    return success


def create_sample_data():
    """サンプルデータを作成"""
    print("\n📊 サンプルデータを作成中...")
    
    os.chdir('backend')
    
    # Activate virtual environment
    if os.name == 'nt':  # Windows
        python_path = "..\\venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_path = "../venv/bin/python"
    
    # Create sample management command
    sample_command = """
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.sister_assistant.models import ChatSession, ChatMessage

class Command(BaseCommand):
    help = 'Create sample data for Sister SaaS'
    
    def handle(self, *args, **options):
        # Create sample user if not exists
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@example.com', 'first_name': 'デモ', 'last_name': 'ユーザー'}
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write('Demo user created')
        
        # Create sample chat session
        session, created = ChatSession.objects.get_or_create(
            user=user,
            title='紗良との初回チャット',
            defaults={'is_active': True}
        )
        
        if created:
            # Add sample messages
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content='お兄ちゃん、こんにちは！紗良だよ。今日は何をお手伝いしようかな？',
                ai_model='claude-3-sonnet'
            )
            
            ChatMessage.objects.create(
                session=session,
                role='user',
                content='こんにちは紗良！今日はPythonのコードレビューをお願いしたいんだ。'
            )
            
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content='お兄ちゃんのコードレビュー、喜んでやるよ！どんなコードか見せて？',
                ai_model='claude-3-sonnet'
            )
            
            self.stdout.write('Sample data created successfully!')
"""
    
    # Create management command directory
    os.makedirs('apps/core/management', exist_ok=True)
    os.makedirs('apps/core/management/commands', exist_ok=True)
    
    # Write __init__.py files
    with open('apps/core/management/__init__.py', 'w') as f:
        f.write('')
    with open('apps/core/management/commands/__init__.py', 'w') as f:
        f.write('')
    
    # Write sample command
    with open('apps/core/management/commands/create_sample_data.py', 'w') as f:
        f.write(sample_command)
    
    # Run the command
    success = run_command(f"{python_path} manage.py create_sample_data")
    
    os.chdir('..')
    return success


def main():
    """メイン処理"""
    print("🎀 Sister SaaS セットアップを開始します！")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        return 1
    
    if not check_dependencies():
        return 1
    
    # Setup steps
    steps = [
        ("仮想環境の作成", create_virtual_environment),
        ("依存関係のインストール", install_requirements),
        ("環境設定のセットアップ", setup_environment),
        ("データベースのセットアップ", setup_database),
        ("サンプルデータの作成", create_sample_data),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ {step_name}に失敗しました")
            return 1
        print(f"✅ {step_name}完了")
    
    print("\n🎉 セットアップが完了しました！")
    print("\n次の手順で開発サーバーを起動してください:")
    print("1. .env ファイルを編集してAPIキーを設定")
    print("2. cd backend")
    
    if os.name == 'nt':  # Windows
        print("3. ..\\venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("3. source ../venv/bin/activate")
    
    print("4. python manage.py runserver")
    print("\nまたは Docker を使用する場合:")
    print("docker-compose up -d")
    
    print("\n💖 紗良がお兄ちゃんを待ってるよ！")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())