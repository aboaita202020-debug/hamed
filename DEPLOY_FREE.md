# تشغيل Hamed مجانًا

## الخيار السريع: Deployka Free Nano

1. افتح Deployka واختر Deploy from GitHub.
2. استخدم مستودع Hamed:
   https://github.com/aboaita202020-debug/hamed
3. اختر branch: `main`.
4. اترك Stack على Python؛ المشروع يحتوي `requirements.txt` و`Dockerfile`.
5. Start command:
   `python bot.py`
6. أضف Environment Variables/Secrets التالية:

- `OPENAI_API_KEY` = مفتاح OpenAI الخاص بك
- `TELEGRAM_BOT_TOKEN` = Token الخاص بـ @mo7hmmed284bot
- `TELEGRAM_CHAT_ID` = `7703641536`
- `HAMED_AUTONOMOUS_MODE` = `true`
- `HAMED_VODAFONE_CASH_WALLET` = `01040900623`

لا تضع Bot Token أو OpenAI key داخل GitHub.

## اختبار التشغيل

بعد نجاح Deploy افتح Telegram وأرسل `/start` إلى `@mo7hmmed284bot`.

ثم أرسل:
`اختبار حامد`

إذا ظهر رد من البوت، فعملية التشغيل الأساسية ناجحة.

## ملاحظة

استضافة مجانية قد تكون مناسبة للتجربة وليست ضمانًا لتشغيل تجاري دائم. يجب التحقق من سياسة الخطة الحالية قبل الاعتماد عليها في الإنتاج.
