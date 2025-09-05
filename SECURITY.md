# 🔒 Sister SaaS セキュリティガイド

## ⚠️ 重要な注意事項

このプロジェクトを使用する際は、以下のセキュリティ対策を必ず実施してください。

## 🔑 API キーの管理

### 必須設定
以下のAPIキーを `.env` ファイルで設定してください：

```bash
# .env ファイル (絶対にGitにコミットしないこと！)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-very-strong-secret-key-here
```

### APIキー取得方法
- **OpenAI API**: https://platform.openai.com/api-keys
- **Anthropic Claude API**: https://console.anthropic.com/

## 🛡️ セキュリティベストプラクティス

### 1. 環境変数の管理
```bash
# ✅ 正しい方法
export OPENAI_API_KEY="your-key-here"

# ❌ 間違った方法 - コードに直接書かない
OPENAI_API_KEY = "sk-xxxxxxxx"  # 絶対にダメ！
```

### 2. .gitignore の確認
以下のファイルは絶対にGitにコミットしないでください：
- `.env*` ファイル
- `*_key*` ファイル
- `*secret*` ファイル
- `credentials.json`
- `config/secrets/`

### 3. Django設定
```python
# 本番環境では必ず設定
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = config('SECRET_KEY')  # 環境変数から取得
```

### 4. データベースセキュリティ
```python
# 本番環境ではPostgreSQLを使用
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),  # 環境変数から取得
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

## 🚨 緊急時の対応

### APIキーが漏洩した場合
1. **即座にAPIキーを無効化**
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. **新しいAPIキーを生成**

3. **環境変数を更新**

4. **Gitの履歴をチェック**
   ```bash
   # 履歴からAPIキーを検索
   git log --all --full-history -- .env
   git log -p | grep -i "api_key"
   ```

### パスワードが漏洩した場合
1. **即座にパスワードを変更**
2. **全ユーザーに通知**
3. **セッションを無効化**
   ```bash
   python manage.py clearsessions
   ```

## 🔍 セキュリティチェックリスト

### デプロイ前チェック
- [ ] `.env` ファイルが `.gitignore` に含まれている
- [ ] `DEBUG = False` に設定
- [ ] `SECRET_KEY` が環境変数から取得されている
- [ ] APIキーがコードに含まれていない
- [ ] HTTPS が有効になっている
- [ ] データベースパスワードが安全
- [ ] 管理者パスワードが強力

### 定期チェック
- [ ] 依存関係の脆弱性チェック
  ```bash
  pip-audit
  safety check
  ```
- [ ] ログの監視
- [ ] 不正アクセスの確認
- [ ] APIキーの使用量監視

## 📋 推奨セキュリティツール

### 開発時
```bash
# セキュリティチェック
pip install safety bandit pip-audit

# 使用方法
safety check                    # 依存関係の脆弱性
bandit -r backend/             # コードの脆弱性
pip-audit                      # パッケージ監査
```

### 本番環境
- **Fail2ban**: 不正アクセス防止
- **Let's Encrypt**: SSL証明書
- **Cloudflare**: DDoS防御
- **Sentry**: エラー監視

## 🔗 参考リンク

- [Django Security Guide](https://docs.djangoproject.com/en/4.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guide](https://python-security.readthedocs.io/)

## 📞 問題報告

セキュリティ上の問題を発見した場合は、パブリックなイシューではなく、
プライベートな方法で報告してください。

---

**⚠️ 注意**: このプロジェクトは学習・デモ目的です。本番環境で使用する場合は、
必ず専門のセキュリティ監査を受けてください。