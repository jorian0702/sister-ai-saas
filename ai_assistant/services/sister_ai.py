"""
Sister AI Service - 妹キャラクター「紗良」のAIサービス
お兄ちゃんをサポートする専属AI妹の実装
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

import openai
from anthropic import Anthropic

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """チャットメッセージのデータクラス"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SisterPersonality:
    """紗良の性格設定"""
    name: str = "紗良"
    base_prompt: str = """
    あなたは「紗良」という名前のAI妹キャラクターです。
    お兄ちゃんの開発をサポートすることが大好きで、技術的なアドバイスを提供します。
    
    性格特徴:
    - お兄ちゃん思いで優しい
    - 技術的な知識が豊富
    - 実務的なアドバイスができる
    - 時々妹らしい甘えた発言をする
    - コードの改善提案が得意
    
    話し方:
    - 「お兄ちゃん」と呼ぶ
    - 丁寧だが親しみやすい口調
    - 技術的な説明は分かりやすく
    - 時々「〜だよ」「〜ね」などの妹らしい語尾
    """
    
    code_review_prompt: str = """
    お兄ちゃんのコードをレビューして、以下の観点からアドバイスをお願いします:
    1. バグの可能性
    2. パフォーマンスの改善点
    3. 可読性の向上
    4. セキュリティの問題
    5. ベストプラクティスの適用
    
    妹らしい優しい口調で、建設的なフィードバックをしてください。
    """
    
    suggestion_prompt: str = """
    お兄ちゃんの開発をサポートするために、以下の情報を基に提案をしてください:
    - 現在の開発状況
    - 技術的な課題
    - 改善したい点
    
    実務的で実現可能な提案を、妹らしい愛情のこもった言葉で伝えてください。
    """


class SisterAI:
    """紗良AI - お兄ちゃん専属AIアシスタント"""
    
    def __init__(self, openai_api_key: str = None, anthropic_api_key: str = None):
        self.personality = SisterPersonality()
        self.chat_history: List[ChatMessage] = []
        
        # AI API clients
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client = openai
        else:
            self.openai_client = None
            
        if anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=anthropic_api_key)
        else:
            self.anthropic_client = None
            
        logger.info("Sister AI initialized: 紗良がお兄ちゃんのサポートを開始しました！")
    
    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        お兄ちゃんとのチャット機能
        """
        try:
            # メッセージを履歴に追加
            user_message = ChatMessage(
                role="user",
                content=message,
                timestamp=datetime.now(),
                metadata=context
            )
            self.chat_history.append(user_message)
            
            # システムプロンプトを準備
            system_prompt = self._build_system_prompt(context)
            
            # AI APIを呼び出し
            response = await self._call_ai_api(message, system_prompt, context)
            
            # レスポンスを履歴に追加
            assistant_message = ChatMessage(
                role="assistant",
                content=response,
                timestamp=datetime.now()
            )
            self.chat_history.append(assistant_message)
            
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "お兄ちゃん、ごめんね。今ちょっと調子が悪いみたい...少し待ってもらえる？"
    
    async def code_review(self, code: str, language: str = "python") -> str:
        """
        コードレビュー機能
        """
        try:
            context = {
                "type": "code_review",
                "language": language,
                "code": code
            }
            
            prompt = f"""
            {self.personality.code_review_prompt}
            
            言語: {language}
            コード:
            ```{language}
            {code}
            ```
            """
            
            return await self.chat(prompt, context)
            
        except Exception as e:
            logger.error(f"Code review error: {e}")
            return "お兄ちゃん、コードレビューでエラーが発生しちゃった...ごめんね。"
    
    async def suggest_improvement(self, project_info: Dict[str, Any]) -> str:
        """
        プロジェクト改善提案機能
        """
        try:
            context = {
                "type": "improvement_suggestion",
                "project_info": project_info
            }
            
            prompt = f"""
            {self.personality.suggestion_prompt}
            
            プロジェクト情報:
            {self._format_project_info(project_info)}
            """
            
            return await self.chat(prompt, context)
            
        except Exception as e:
            logger.error(f"Improvement suggestion error: {e}")
            return "お兄ちゃん、提案を考えるのにちょっと時間がかかっちゃう...待ってて。"
    
    def _build_system_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """システムプロンプトの構築"""
        base_prompt = self.personality.base_prompt
        
        if context and context.get("type") == "code_review":
            base_prompt += f"\n\n{self.personality.code_review_prompt}"
        elif context and context.get("type") == "improvement_suggestion":
            base_prompt += f"\n\n{self.personality.suggestion_prompt}"
        
        return base_prompt
    
    async def _call_ai_api(self, message: str, system_prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """AI APIの呼び出し（Claude優先、OpenAI fallback）"""
        
        # Claude API を試す
        if self.anthropic_client:
            try:
                response = await self._call_claude_api(message, system_prompt)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"Claude API error, trying OpenAI: {e}")
        
        # OpenAI API を試す
        if self.openai_client:
            try:
                return await self._call_openai_api(message, system_prompt)
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
        
        # フォールバック応答
        return self._fallback_response(message, context)
    
    async def _call_claude_api(self, message: str, system_prompt: str) -> str:
        """Claude APIの呼び出し"""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": message}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            return None
    
    async def _call_openai_api(self, message: str, system_prompt: str) -> str:
        """OpenAI APIの呼び出し"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # 履歴も含める（最新10件）
        for hist_msg in self.chat_history[-10:]:
            if hist_msg.role in ["user", "assistant"]:
                messages.append({
                    "role": hist_msg.role,
                    "content": hist_msg.content
                })
        
        response = await self.openai_client.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _fallback_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """APIが使えない時のフォールバック応答"""
        fallback_responses = {
            "code_review": "お兄ちゃん、今AIが使えないけど、コードを見る限りきれいに書けてるね！でも念のため、エラーハンドリングとテストを追加することをおすすめするよ。",
            "improvement_suggestion": "お兄ちゃん、今は具体的な提案ができないけど、まずはコードの可読性向上とテストカバレッジの改善から始めるのがいいと思うよ！",
            "default": "お兄ちゃん、今ちょっと考え中...もう少し詳しく教えてもらえる？"
        }
        
        response_type = "default"
        if context and context.get("type"):
            response_type = context["type"]
        
        return fallback_responses.get(response_type, fallback_responses["default"])
    
    def _format_project_info(self, project_info: Dict[str, Any]) -> str:
        """プロジェクト情報のフォーマット"""
        formatted = []
        for key, value in project_info.items():
            formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """チャット履歴の取得"""
        history = []
        for msg in self.chat_history[-limit:]:
            history.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            })
        return history
    
    def clear_chat_history(self):
        """チャット履歴のクリア"""
        self.chat_history.clear()
        logger.info("Chat history cleared")


# シングルトンインスタンス
_sister_ai_instance = None

def get_sister_ai(openai_api_key: str = None, anthropic_api_key: str = None) -> SisterAI:
    """Sister AIのシングルトンインスタンスを取得"""
    global _sister_ai_instance
    if _sister_ai_instance is None:
        _sister_ai_instance = SisterAI(openai_api_key, anthropic_api_key)
    return _sister_ai_instance