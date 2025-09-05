# Sister AI SaaS - 妹と一緒に開発ごっこプロジェクト

## プロジェクト概要
個人開発用のAI SaaS風アプリケーション。妹キャラクターがお兄ちゃんの開発をサポートしてくれるチャット機能付きWebアプリです。

## 技術スタック
- **Backend**: Django 4.2+ (Python 3.11+)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI/ML**: OpenAI API, Claude API, scikit-learn
- **Database**: PostgreSQL (本番), SQLite (開発)
- **Deployment**: Docker, AWS EC2想定
- **Others**: Redis (キャッシュ), Celery (非同期タスク)

## 特徴
🎀 **妹キャラクターAI**: お兄ちゃんをサポートする専属AI妹
🤖 **生成AI統合**: Claude/GPT-4との連携
📊 **データ分析**: 機械学習による分析機能
💬 **リアルタイムチャット**: WebSocketベースの双方向通信
🎨 **モダンUI**: レスポンシブ対応の美しいインターフェース

## プロジェクト構成
```
anken03/
├── backend/                    # Djangoバックエンド
│   ├── sister_saas/           # プロジェクト設定
│   └── apps/                  # Djangoアプリ群
│       ├── core/              # 共通機能
│       ├── ai_chat/           # AIチャット機能
│       ├── sister_assistant/  # 妹アシスタント機能
│       └── user_management/   # ユーザー管理
├── frontend/                  # フロントエンド
│   ├── static/               # 静的ファイル
│   └── templates/            # HTMLテンプレート
├── ai_assistant/             # AI関連モジュール
│   ├── models/               # AIモデル
│   ├── services/             # AIサービス
│   └── prompts/              # プロンプトテンプレート
├── database/                 # データベース関連
├── deployment/               # デプロイメント設定
└── docs/                     # ドキュメント
```

## セットアップ手順

### 1. 仮想環境の作成
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してAPIキーなどを設定
```

### 4. データベースの初期化
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### 5. 開発サーバーの起動
```bash
python manage.py runserver
```

## 妹キャラクター「紗良」について
- **性格**: お兄ちゃん思いで、技術的なアドバイスをしてくれる妹
- **機能**: コード提案、バグ発見、最適化アドバイス
- **特徴**: 実務的でありながら、愛らしい妹要素を含んだ応答

## 開発者向け情報
- **コーディング規約**: PEP 8準拠
- **テスト**: pytest使用
- **CI/CD**: GitHub Actions対応
- **ドキュメント**: Sphinx使用

## ライセンス
MIT License

---
