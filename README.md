# Hamed AI — دليل التشغيل

نظام Multi-Agent Business Operating System. الـ Core لا يحتاج أي مكتبة
خارجية (Python stdlib فقط) — كل شيء آخر (Telegram, Dashboard API, AI
Providers) طبقات اختيارية منفصلة.

## 1) التشغيل محليًا بدون Docker

```bash
python3 -m venv venv
source venv/bin/activate        # على ويندوز: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # عدّل القيم اللي محتاجها بس
python -m unittest discover -s tests -v   # للتأكد إن كل حاجة شغالة
python scripts/run_server.py     # يفتح على http://127.0.0.1:8000
```

نقاط الوصول:
- `GET /health` — فحص حياة السيرفر.
- `GET /readiness` — فحص جاهزية قاعدة البيانات.
- `GET /dashboard` — ملخص الأداء (Leads, Opportunities, Revenue).
- `GET /leads`, `GET /opportunities`, `GET /audit-logs`
- `POST /dispatch/{agent_name}` — تشغيل أي Agent يدويًا (body: JSON payload).

لتشغيل بوت تليجرام (بعد ضبط `TELEGRAM_BOT_TOKEN` في `.env`):
```bash
python scripts/run_telegram.py
```

## 2) التشغيل عبر Docker (بدون الحاجة لـ Docker على جهازك)

بما إن **Docker Desktop لا يدعم Windows 7** (يحتاج Windows 10/11 مع
WSL2)، الطريقة المضبوطة هنا هي إن GitHub نفسه يبني صورة الـ Docker
وينشرها، مش جهازك:

1. ارفع الكود على مستودع GitHub جديد (فارغ الأول، عادي).
2. الملف `.github/workflows/docker-publish.yml` موجود جاهز — أول ما
   تعمل `git push` على فرع `main`، GitHub Actions هيشغّل الاختبارات
   تلقائيًا، وبعدين يبني صورة Docker وينشرها على
   `ghcr.io/<اسم-المستخدم>/<اسم-المستودع>:latest`.
3. من إعدادات المستودع على GitHub: Settings → Packages، تأكد إن الصورة
   ظاهرة بعد أول Push ناجح (تقدر كمان تتابع التقدم من تبويب Actions).
4. في `justrunmy.app` (أو أي منصة Docker تانية)، وجّهها لسحب الصورة من
   `ghcr.io/<اسم-المستخدم>/<اسم-المستودع>:latest` بدل ما تعمل
   `docker build`/`push` بنفسك.
   - لو المنصة محتاجة الصورة على Docker Hub تحديدًا بدل GHCR، فعّل
     الجزء المعلّق (commented) في نفس ملف الـ workflow وضيف
     `DOCKERHUB_USERNAME` و `DOCKERHUB_TOKEN` كـ Secrets في إعدادات
     المستودع (Settings → Secrets and variables → Actions).
5. اضبط متغيرات البيئة (نفس اللي في `.env.example`) من لوحة تحكم
   المنصة نفسها — منها التوكن، مفاتيح الـ AI، وحدود الموافقات.
6. اعمل Mount لمجلد `/app/data` كـ Volume دائم لو المنصة بتدعم كده، عشان
   بيانات الـ CRM متضيعش عند إعادة تشغيل الحاوية.

## 3) البنية

```
app/
  config.py            # كل الإعدادات من Environment Variables
  db/                   # SQLite (stdlib) + Repository + CRM Dedup + Audit Log
  permissions/           # Permission Layer / Approval Gate
  tools/                 # Tool Registry + WebSearchTool + CRMTool
  agents/
    orchestrator.py      # HamedOrchestrator
    *_agent.py            # كل Agent قابل للاختبار منفردًا
  ai_providers/          # Router + Fallback بين المزودين
  channels/telegram_adapter.py   # اختياري
  api/server.py                    # اختياري (FastAPI)
scripts/
  run_server.py           # نقطة تشغيل الـ Dashboard/Webhook
  run_telegram.py         # نقطة تشغيل بوت تليجرام (Polling)
tests/                     # 23 اختبار unittest (stdlib فقط، بدون أي pip install)
```

## 4) قاعدة أساسية

كل Agent وكل Tool بيتحقنوا (dependency injection) بدل الاستيراد
المباشر — عشان تقدر تضيف Agent جديد أو تستبدل قاعدة البيانات من غير
ما تلمس بقية الكود. راجع `app/agents/orchestrator.py` لمعرفة إزاي
تسجّل Agent جديد عبر `register_agent()`.

## 5) الخطوة الجاية المقترحة

الوثيقة الأصلية بتحدد 17 Phase. اللي اتنفذ فعليًا دلوقتي يغطي:
Phase 1 (Core مستقر بدون ImportError)، Phase 3 (Agent/Tool Interfaces +
Orchestrator)، جزء من Phase 4 (CRM)، جزء من Phase 5 (Sales)، جزء من
Phase 6 (Opportunity Hunter)، جزء من Phase 7 (Revenue)، جزء من Phase 9
(Negotiation + Approval)، جزء من Phase 10 (Dashboard كـ JSON API)، وكل
من Phase 2 و14 و15 (Telegram أساسي، CI عبر GitHub Actions، Docker).

لسه محتاج: Purchasing Engine، Web/Social Intelligence حقيقي (بدل الـ
mock provider)، RAG/Knowledge Base، WhatsApp/Voice، Dashboard UI بصري
(الحالي JSON فقط).
