#!/usr/bin/env python3
"""
agent.py
وكيل بسيط يحتفظ بسياق المحادثة في الذاكرة (قائمة من أدوار المستخدم/المساعد).
يدعم استدعاء Anthropic Claude عبر الحزمة الرسمية إن كانت متاحة.
ملاحظة: للمشاريع الحقيقية استخدم تخزين دائم (DB) وقيود للمحافظة على التكاليف.
"""
import os
from typing import List, Dict

# حاول استخدام الحزمة الرسمية أولًا، وإلا فارتكز على طلبات HTTP حسب تفضيلك.
try:
    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
    _HAS_ANTHROPIC = True
except Exception:
    _HAS_ANTHROPIC = False

import requests

DEFAULT_MODEL = "claude-2"  # عدّل هذا إن لزم حسب إصدارات Anthropic

class Agent:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL, max_tokens: int = 1000):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        # سياق بسيط: قائمة من dicts: {"role": "user"/"assistant", "content": "..."}
        self.conversation: List[Dict[str,str]] = []

        if _HAS_ANTHROPIC:
            self.client = Anthropic(api_key=api_key)
        else:
            self.client = None

    def reset(self):
        self.conversation = []

    def _build_prompt(self, user_message: str) -> str:
        # بناء Prompt بصيغة Anthropic (HUMAN_PROMPT / AI_PROMPT) لتضمين التاريخ الكامل للمحادثة
        # ندمج الرسائل التاريخية ثم الرسالة الحالية
        if _HAS_ANTHROPIC:
            parts = []
            for turn in self.conversation:
                if turn["role"] == "user":
                    parts.append(HUMAN_PROMPT + " " + turn["content"] + "\n")
                else:
                    parts.append(AI_PROMPT + " " + turn["content"] + "\n")
            parts.append(HUMAN_PROMPT + " " + user_message + "\n\n" + AI_PROMPT + " ")
            return "".join(parts)
        else:
            # بديل عام: سلسلة نصية تتضمن الأدوار
            history = ""
            for turn in self.conversation:
                history += f"{turn['role'].upper()}: {turn['content']}\n"
            history += f"USER: {user_message}\nASSISTANT: "
            return history

    def _call_anthropic(self, prompt: str) -> str:
        if _HAS_ANTHROPIC and self.client:
            # استخدام الحزمة الرسمية (قد تختلف الواجهة حسب نسخة الحزمة)
            try:
                resp = self.client.completions.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens_to_sample=self.max_tokens,
                )
                # قد يكون الحقل: resp["completion"] أو resp.completion بحسب النسخة
                completion = None
                if isinstance(resp, dict):
                    completion = resp.get("completion") or resp.get("text")
                else:
                    # كائن مع خاصية completion
                    completion = getattr(resp, "completion", None) or getattr(resp, "text", None)
                return completion.strip() if completion else "لم يأتِ رد من Anthropic."
            except Exception as e:
                raise RuntimeError(f"Anthropic client error: {e}")
        else:
            # بديل HTTP بسيط — قد يحتاج تكييف حسب التوثيق الفعلي (Authorization header أو x-api-key)
            url = "https://api.anthropic.com/v1/complete"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,  # إن كان موثوقًا في حسابك؛ البعض يستخدم Authorization: Bearer <KEY>
            }
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens_to_sample": self.max_tokens,
            }
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            if not r.ok:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text}")
            data = r.json()
            # الحقل المتوقع غالبًا "completion"
            completion = data.get("completion") or data.get("completion_text") or data.get("text") or ""
            return completion.strip()

    def get_response(self, user_message: str) -> str:
        # تضيف رسالة المستخدم إلى السياق، تنادي Anthropic، تحفظ الرد وتعيده
        self.conversation.append({"role": "user", "content": user_message})
        prompt = self._build_prompt(user_message)
        reply = self._call_anthropic(prompt)
        self.conversation.append({"role": "assistant", "content": reply})
        # تقييد طول المحادثة (اختياري) — هنا نحتفظ بآخر 20 رسالة
        if len(self.conversation) > 40:
            self.conversation = self.conversation[-40:]
        return reply
