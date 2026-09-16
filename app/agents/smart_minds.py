"""Hamed's business-specialist mind catalog.

These are capability profiles used by the orchestrator/UI. They are not separate
LLMs by themselves; the configured provider layer supplies the underlying model.
"""
from __future__ import annotations

SMART_MINDS = [
    {"id": "central_council", "name": "Central Council", "ar": "مجلس العقول والقرار", "icon": "🧠", "description": "يجمع آراء العقول ويحوّلها إلى قرار وخطة قابلة للتنفيذ."},
    {"id": "opportunity_hunter", "name": "Opportunity Hunter", "ar": "صياد الفرص", "icon": "🎯", "description": "يكتشف فرص الأعمال والربح ويضعها في قائمة تحقق."},
    {"id": "sales", "name": "Sales", "ar": "المبيعات", "icon": "💵", "description": "يبني عروض البيع ويؤهل العملاء ويتابع دورة البيع."},
    {"id": "purchasing", "name": "Purchasing", "ar": "المشتريات والموردون", "icon": "🛒", "description": "يقارن الموردين والأسعار وشروط الشراء وإعادة البيع."},
    {"id": "negotiation", "name": "Negotiation", "ar": "التفاوض", "icon": "🤝", "description": "يصمم استراتيجيات تفاوض وحدود سعر آمنة."},
    {"id": "customer_psychology", "name": "Customer Psychology", "ar": "سيكولوجية العميل", "icon": "🧩", "description": "يفهم احتياج العميل ودوافعه واعتراضاته دون تلاعب."},
    {"id": "customer_relationship", "name": "Customer Relationship", "ar": "علاقات العملاء", "icon": "❤️", "description": "يدير التواصل والمتابعة والاحتفاظ بالعملاء."},
    {"id": "marketing", "name": "Marketing", "ar": "التسويق", "icon": "📣", "description": "يخطط للحملات والرسائل والقنوات ومؤشرات القياس."},
    {"id": "affiliate", "name": "Affiliate Growth", "ar": "التسويق بالعمولة", "icon": "🔗", "description": "يبحث ويقيّم برامج العمولة ويبني اختبارات قابلة للقياس."},
    {"id": "b2b", "name": "B2B Brokerage", "ar": "وساطة B2B", "icon": "🏢", "description": "يربط احتياجات الشركات بالموردين والعملاء المحتملين."},
    {"id": "website_factory", "name": "Website Factory", "ar": "مصنع المواقع والمتاجر", "icon": "🌐", "description": "يحلل المتاجر ويخطط لإنشاء وتحسين المواقع وصفحات البيع."},
    {"id": "lead_discovery", "name": "Lead Discovery", "ar": "اكتشاف العملاء المحتملين", "icon": "🔎", "description": "يحدد مصادر العملاء المحتملين ويجهز قوائم تواصل مشروعة."},
    {"id": "research", "name": "Research", "ar": "البحث والاستخبارات", "icon": "🔬", "description": "يجمع المعلومات ويقارن المصادر ويحدد ما يحتاج تحققًا."},
    {"id": "economic_intelligence", "name": "Economic Intelligence", "ar": "الاستخبارات الاقتصادية", "icon": "📈", "description": "يحلل الأسعار والطلب والمنافسة والفرص الاقتصادية."},
    {"id": "revenue", "name": "Revenue Architect", "ar": "هندسة الإيرادات", "icon": "💰", "description": "يبني قنوات دخل متعددة ويقيس جدواها ومراحل اختبارها."},
    {"id": "learning", "name": "Learning", "ar": "التعلم المستمر", "icon": "📚", "description": "يحوّل نتائج المهام والمصادر الموثوقة إلى معرفة قابلة لإعادة الاستخدام."},
    {"id": "memory", "name": "Memory", "ar": "الذاكرة", "icon": "🗃️", "description": "يحافظ على سياق المشاريع والعملاء والقرارات والنتائج."},
    {"id": "execution", "name": "Execution", "ar": "التنفيذ والمهام", "icon": "⚙️", "description": "يقسم الأهداف إلى مهام ويتابع الحالة والنتائج ضمن الصلاحيات."},
    {"id": "risk_guard", "name": "Risk & Approval Guard", "ar": "الحماية وإدارة المخاطر", "icon": "🛡️", "description": "يمنع الإجراءات الحساسة دون الصلاحية والموافقة المطلوبة."},
    {"id": "quality", "name": "Quality & Optimization", "ar": "الجودة والتحسين", "icon": "✅", "description": "يفحص النتائج ويقترح التحسينات ويكشف التناقضات والأخطاء."},
]


def list_smart_minds() -> list[dict[str, str]]:
    return [dict(mind, status="active") for mind in SMART_MINDS]
