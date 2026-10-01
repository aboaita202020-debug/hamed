# 🤖 Freelance Automation System

نظام أتمتة خدمات Freelancing باستخدام 6 AI brains

## 🎯 نظرة عامة

النظام بيستخدم 6 عقول اصطناعية لتقديم خدمات Freelancing على منصات زي Fiverr, Upwork, Mostaql

### الخدمات المدعومة:
- ✅ **كتابة محتوى** (مقالات، SEO)
- ✅ **ترجمة** (EN ↔ AR)
- ✅ **تحليل بيانات** (تقارير)
- ✅ **برمجة** (أكواد بسيطة)

## 🏗️ البنية

```
freelance_automation/
├── core/
│   ├── config.py          # إعدادات النظام
│   ├── database.py        # SQLite database
│   └── logger.py          # Logging system
├── ai_brains/
│   └── brain_router.py    # توزيع المهام على 6 عقول
├── tests/
│   └── test_system.py     # اختبارات النظام
├── main.py                # CLI interface
├── requirements.txt       # المتطلبات
└── .env.example          # مثال الإعدادات
```

## 🚀 التشغيل

### 1. ثبّت Python 3.8+
```bash
python --version  # لازم 3.8 أو أحدث
```

### 2. انسخ ملف الإعدادات
```bash
cd freelance_automation
cp .env.example .env
```

### 3. عدّل ملف .env
```bash
# حط API keys للـ 6 عقول
BRAIN_1_API_KEY=your_key_here
BRAIN_2_API_KEY=your_key_here
# ... إلخ
```

### 4. تحقق من الإعدادات
```bash
python main.py validate
```

### 5. شغّل الاختبارات
```bash
python -m unittest discover -s tests -v
```

## 🔄 التشغيل التلقائي 24/7

### الطريقة 1: يدوي (Simple)
```bash
# شغّل الخدمة
python service_247.py

# أو من CMD
python main.py service
```

### الطريقة 2: Windows Service (Recommended)
```bash
# 1. ثبّت الخدمة (Run as Administrator)
INSTALL_SERVICE.bat

# 2. شغّل الخدمة يدوي
START_247.bat

# 3. شوف الحالة
STATUS.bat

# 4. وقف الخدمة
STOP_SERVICE.bat
```

### الطريقة 3: Scheduled Task (Auto-Start)
```bash
# الخدمة هتشتغل تلقائي لما تعمل login
# مش محتاج تعمل حاجة بعد INSTALL_SERVICE.bat
```

### مميزات التشغيل 24/7:
- ✅ يراقب المنصات تلقائياً كل 5 دقائق
- ✅ يعالج الطلبات الجديدة كل دقيقة
- ✅ يسلم الطلبات تلقائياً
- ✅ يتتبع الإيرادات
- ✅ يشتغل في الخلفية
- ✅ يبدأ تلقائي مع Windows

## 📋 الاستخدام

### إنشاء طلب جديد
```bash
python main.py create-order \
  --platform fiverr \
  --service content_writing \
  --client "Ahmed" \
  --description "Write SEO article about AI" \
  --price 15.0
```

### معالجة الطلب بالـ AI
```bash
python main.py process-order ORD-20260108-123456
```

### تسليم الطلب
```bash
python main.py deliver-order ORD-20260108-123456
```

### عرض الإحصائيات
```bash
python main.py dashboard
```

### عرض حالة العقول
```bash
python main.py brains
```

## 🧠 العقول الستة

| Brain | الاسم | التخصص |
|-------|------|--------|
| brain_1 | Content Writer | إنشاء محتوى |
| brain_2 | Translator | ترجمة |
| brain_3 | Data Analyst | تحليل بيانات |
| brain_4 | Code Generator | برمجة |
| brain_5 | Quality Checker | فحص جودة |
| brain_6 | Optimizer | تحسين |

## 💰 الدخل المتوقع

- **شهر 1-2**: $100-500
- **شهر 3-6**: $500-2000
- **شهر 7-12**: $2000-5000

## ⚙️ المتطلبات

- Python 3.8+
- 6 AI API keys (Anthropic, OpenAI, etc.)
- SQLite (مدمج في Python)

## 📝 ملاحظات مهمة

1. **النسخة الحالية**: Mock implementation - محتاج تضيف API integration حقيقي
2. **المنصات**: محتاج API keys من Fiverr, Upwork, Mostaql
3. **الجودة**: نظام فحص الجودة محتاج تطوير

## 🔧 التطوير

### إضافة خدمة جديدة
1. أضف الخدمة في `config.py`
2. أضف task type في `brain_router.py`
3. أضف tests

### إضافة Brain جديد
1. أضف brain في `config.py`
2. أضف specialty mapping في `brain_router.py`

## 📄 الترخيص

MIT License

## 🔗 الروابط

- [PROJECT_MAP.md](./PROJECT_MAP.md) - خريطة المشروع الكاملة
- [المستودع الأصلي](https://github.com/aboaita202020-debug/hamed)
