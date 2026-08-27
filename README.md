# 🤖 بوت تليجرام ذكي مبني على Claude (MVP)

بوت تليجرام (نسخة MVP) بيستخدم Claude من Anthropic كوكيل ذكي واحد، بيحتفظ بسياق المحادثة، وقابل للتوسع لاحقًا لمشروع أكبر (قاعدة بيانات، عدة وكلاء، Dashboard... إلخ).

## الملفات
- bot.py — نقطة التشغيل (polling)
- agent.py — طبقة الوكيل التي تتكلم مع Anthropic وتحفظ السياق
- requirements.txt — المكتبات المطلوبة
- .env.example — نموذج متغيرات بيئة

## التشغيل
1. انسخ `.env.example` إلى `.env` واملأ المفاتيح:
   cp .env.example .env
2. ثبت المتطلبات:
   pip install -r requirements.txt
3. شغّل البوت:
   python bot.py
4. جرّب إرسال /start أو أي رسالة لبوتك في Telegram.

## ملاحظات
- الكود يستخدم polling (سهُل للتشغيل محليًا). للـ production يفضل Webhooks.
- احفظ مفاتيحك سرية ولا ترفع `.env` إلى GitHub.
- للحفاظ على المحادثات بشكل دائم استخدم قاعدة بيانات (Postgres أو غيرها).
