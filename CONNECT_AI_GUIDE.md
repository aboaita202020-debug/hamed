# 🤖 دليل ربط AI APIs - خطوة بخطوة

## 🎯 الخطوات بالترتيب

### ✅ الخطوة 1: تأكد من تثبيت Python
```bash
python --version
```
- لو ظهر رقم ✅ تمام
- لو ظهر خطأ ❌ حمّل من: https://www.python.org/downloads/

### ✅ الخطوة 2: تأكد من ملف .env
```bash
# افتح ملف .env وتأكد إن فيه المفاتيح دي:
ANTHROPIC_API_KEY=sk-ant-api03--1Y...mAAA
OPENAI_API_KEY=key_C8KiWEvc7gnmHzxF
KIMI_API_KEY=sk-ED3y5vB94bDj4bbKOEAlmUEhxRbHgu2btFr9pi2L3g4mU1Cc
GEMINI_API_KEY=AQ.Ab8RN6JVT1IzAnxTiHS4xZ4vWo8Bgsb2m-8k_aBhpIRW-cbU6w
TELEGRAM_BOT_TOKEN=8843221025:AAGtegewAMOalwv1ZAlBlCKwjPI953vfJuU
```

### ✅ الخطوة 3: شغّل ملف الربط
```bash
# دبل كليك على CONNECT_AI.bat
# أو من CMD:
CONNECT_AI.bat
```

**الملف ده هيعمل:**
1. ✅ يثبّت المكتبات المطلوبة تلقائياً
2. ✅ يختبر كل الـ APIs
3. ✅ يوريك أي API شغال وأي لأ
4. ✅ يسألك لو عايز تشغل البوت

### ✅ الخطوة 4: شغّل البوت
```bash
# دبل كليك على START_BOT.bat
# أو من CMD:
START_BOT.bat
```

### ✅ الخطوة 5: جرب البوت
1. افتح تيليجرام
2. ابحث عن: `@hamed_ai_bot`
3. ابعت: `/start`
4. البوت هيرد عليك بذكاء اصطناعي! 🤖

---

## 🧪 اختبار الـ APIs يدوياً

لو عايز تختبر الـ APIs بنفسك:

```bash
# من CMD في مجلد freelance_automation:
cd freelance_automation
python test_apis.py
```

**النتيجة المتوقعة:**
```
============================================================
🧪 اختبار AI APIs
============================================================

1️⃣  اختبار Anthropic Claude...
✅ Anthropic شغال!
   الرد: مرحباً! كيف يمكنني مساعدتك اليوم؟...

2️⃣  اختبار OpenAI GPT-4...
✅ OpenAI شغال!
   الرد: مرحباً! أنا هنا لمساعدتك...

3️⃣  اختبار Kimi Moonshot...
✅ Kimi شغال!
   الرد: مرحباً! كيف أقدر أساعدك؟...

4️⃣  اختبار Google Gemini...
✅ Gemini شغال!
   الرد: مرحباً! أنا Gemini...

============================================================
✅ انتهى الاختبار!
============================================================
```

---

## 📋 المكتبات المطلوبة

### المكتبات الأساسية:
```bash
pip install python-dotenv anthropic openai requests python-telegram-bot
```

### أو من ملف requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 🔧 حل المشاكل

### المشكلة: "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip install anthropic
```

### المشكلة: "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### المشكلة: "ModuleNotFoundError: No module named 'telegram'"
```bash
pip install python-telegram-bot
```

### المشكلة: "Unauthorized" أو "Invalid API key"
- تأكد إن المفاتيح في .env صحيحة
- تأكد إن المفاتيح فعّالة ومش منتهية
- جرّب تعمل مفتاح جديد من موقع الـ API

### المشكلة: "Connection timeout"
- تأكد إن عندك إنترنت
- تأكد إن الـ API مش محجوب في بلدك
- جرّب تستخدم VPN

---

## 🎯 ترتيب الـ APIs

البوت بيحاول يستخدم الـ APIs بالترتيب ده:

1. **Anthropic Claude** (الأفضل للجودة)
2. **OpenAI GPT-4** (بديل ممتاز)
3. **Kimi Moonshot** (سريع وفعال)
4. **Google Gemini** (مجاني وقوي)
5. **ردود جاهزة** (لو كل الـ APIs فشلت)

---

## 💡 نصائح مهمة

### 1. حماية المفاتيح
- ✅ المفاتيح في .env فقط
- ✅ .gitignore يمنع رفعها على GitHub
- ❌ لا تشارك مفاتيحك مع أي شخص

### 2. توفير التكلفة
- استخدم Anthropic Claude للمهام المعقدة
- استخدم OpenAI GPT-4 للمهام المتوسطة
- استخدم Kimi أو Gemini للمهام البسيطة

### 3. المراقبة
- شوف سجل المحادثات في قاعدة البيانات
- تابع أي API بيشتغل أكتر
- حسّن الردود بناءً على تفاعلات العملاء

---

## 📞 معلومات التواصل

- **واتساب**: 01061245527
- **فودافون كاش**: 01040900623
- **تيليجرام**: @hamed_ai_bot

---

## 🎊 الخلاصة

**الخطوات:**
1. ✅ تأكد من Python
2. ✅ تأكد من .env
3. ✅ شغّل CONNECT_AI.bat
4. ✅ شغّل START_BOT.bat
5. ✅ جرب البوت في تيليجرام

**يلا نبدأ!** 🚀💰
