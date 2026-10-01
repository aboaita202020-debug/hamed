"""The 95 numbered monetization ideas present in Hamed's income plan."""
from __future__ import annotations

CATEGORIES = {
1: "خدمات محتوى وسوشيال ميديا",
2: "خدمات مواقع ومتاجر إلكترونية",
3: "بيع/شراء ووساطة تجارية",
4: "Affiliate ومحتوى ترويجي",
5: "خدمات فريلانس ووساطة مواهب",
6: "استيراد وتصدير",
7: "تصنيع ومصانع",
8: "شراكات وMarketplace",
9: "تحليل سوق ومنافسين",
10: "بناء منتجات وSaaS",
11: "تجارب وقرارات Scale/Kill",
12: "تعليم ومحتوى تعليمي",
13: "سوشيال ميديا لكل منصة على حدة",
14: "تحقق وحماية",
15: "مبيعات وتفاوض كخدمة",
16: "بحث عن عملاء وLeads كخدمة",
17: "الدفع والتحصيل كخدمة مساندة",
18: "تقارير وبيانات",
19: "قطاعات متخصصة",
20: "نماذج اشتراك متكررة",
}

# id|category|idea|agents. Empty agent fields are intentional: the source did not name an agent.
_RAW = '''
1|1|باقة 4 بوستات شهريًا لمحل صغير|marketing_agent
2|1|باقة يومية (بوست كل يوم) لصفحة بيزنس نشطة|marketing_agent
3|1|سكريبتات فيديو Reels/TikTok جاهزة|video_content_agent
4|1|Storyboard كامل لإعلان فيديو|video_content_agent
5|1|كتابة تعليقات ردود جاهزة على استفسارات متكررة|faq_education_agent
6|1|تقويم محتوى شهر كامل مسبقًا|marketing_agent
7|1|صياغة Captions بلهجات مختلفة (مصري/خليجي/فصحى)|marketing_agent
8|1|كتابة نصوص إعلانات مدفوعة (Facebook/Instagram Ads copy)|marketing_agent
9|1|تجديد هوية المحتوى لصفحة قديمة (Rebranding Copy)|marketing_agent
10|1|باقة "استغاثة" لصفحة هابطة تفاعلها — تحليل + محتوى|market_competitor_agent,marketing_agent
11|2|صفحة هبوط سريعة ليوم واحد|websiteless_business_agent
12|2|كتالوج منتجات لمتجر أونلاين|websiteless_business_agent
13|2|صفحة "من نحن" احترافية لموقع موجود|websiteless_business_agent
14|2|نصوص صفحة الأسئلة الشائعة (FAQ) لموقع|faq_education_agent
15|2|مراجعة وتحسين نصوص متجر إلكتروني موجود|marketing_agent,market_competitor_agent
16|2|بناء متجر Shopify/Salla بسيط كخدمة كاملة (يدوي + مساعدة حامد بالنصوص)|
17|2|صفحة حجز مواعيد بسيطة لعيادة/صالون (لا كود، أدوات جاهزة زي Calendly)|
18|3|الوساطة بين مورد ومشتري بعمولة|lead_generation_agent
19|3|Dropshipping من مورد محلي لعميل نهائي|purchasing_agent,sales_agent
20|3|إعادة بيع منتجات بالجملة بهامش ربح|purchasing_agent
21|3|مقارنة أسعار موردين لعميل مقابل رسوم استشارة|purchasing_agent
22|3|تقييم عروض شراء وحساب هامش الربح لتاجر|purchasing_agent
23|3|خدمة "دورينا لك أرخص مورد" برسم ثابت|purchasing_agent,manufacturing_agent
24|3|توصيل عروض تصفية/كسر سعر بين تجار|partnership_marketplace_agent
25|3|عمولة على صفقات B2B تتم عن طريقك|lead_generation_agent
26|4|الترويج لمنتجات Amazon Associates بمحتوى|affiliate_agent,marketing_agent
27|4|مراجعات منتجات مدفوعة (Sponsored Reviews)|affiliate_agent
28|4|بناء صفحة مقارنة منتجات مع روابط عمولة|affiliate_agent,websiteless_business_agent
29|4|حساب أفضل برامج Affiliate حسب العائد المتوقع|affiliate_agent
30|4|حملة بريد إلكتروني ترويجية لمنتج Affiliate| 
31|5|توصيل فريلانسر مناسب لمشروع مقابل عمولة|freelance_agent
32|5|تسعير مشروع فريلانس بشكل عادل للطرفين|freelance_agent
33|5|كتابة عروض تقديم للمشاريع (Proposals)|freelance_agent,marketing_agent
34|5|بناء فريق فريلانسرز صغير تديره وتاخد نسبة|freelance_agent
35|5|مراجعة أسعار السوق لخدمة فريلانس معينة|market_competitor_agent
36|6|حساب التكلفة النهائية (Landed Cost) لمستورد صغير|import_export_agent
37|6|اقتراح أسواق تصدير لمنتج محلي|import_export_agent
38|6|خدمة استشارية "هل السلعة دي تستاهل تستوردها؟"|import_export_agent,market_competitor_agent
39|6|ربط مصانع محلية بمستوردين خارجيين|lead_generation_agent
40|7|ترتيب أفضل مصنع حسب السعر والجودة لعميل|manufacturing_agent
41|7|حساب تكلفة الوحدة حسب حجم الطلب (Economies of Scale)|manufacturing_agent
42|7|وساطة بين علامة تجارية صغيرة ومصنع تصنيع خاص (Private Label)|manufacturing_agent,lead_generation_agent
43|8|تقييم شراكة محتملة قبل التوقيع|partnership_marketplace_agent
44|8|ترتيب فرص Marketplace حسب القيمة المتوقعة|partnership_marketplace_agent
45|8|بناء شبكة شركاء توزيع محليين|partnership_marketplace_agent
46|9|تقرير منافسين لمشروع ناشئ|market_competitor_agent
47|9|تقدير حجم سوق قبل إطلاق منتج|market_competitor_agent
48|9|تحليل SWOT سريع لبيزنس صغير|market_competitor_agent
49|9|باقة "افهم منافسك في يوم" — تقرير مدفوع سريع|market_competitor_agent
50|10|تقييم فكرة SaaS قبل ما تبدأي فيها لعميل|product_builder_agent
51|10|كتابة مواصفات MVP لفكرة منتج|product_builder_agent
52|10|استشارة "هل الفكرة دي تستاهل وقتك؟"|product_builder_agent
53|10|بناء أداة SaaS بسيطة فعليًا (حاسبة، مولد، محول) وبيعها كاشتراك شهري صغير|
54|11|استشارة "أوقف الحملة دي ولا أكمل؟" مبنية على بيانات حقيقية|experiment_engine
55|11|تقييم قناة تسويقية جديدة قبل ما تستثمري فيها فلوس|experiment_engine
56|12|شرح منتج معقد بطريقة بسيطة للعملاء|product_education_agent
57|12|دليل Onboarding لعملاء جدد|onboarding_education_agent
58|12|صفحة أسئلة شائعة كاملة|faq_education_agent
59|12|رد تعليمي على اعتراض شائع بدون ضغط بيعي|objection_education_agent
60|12|تقرير تعليمي عن اتجاه في السوق (Newsletter مدفوع)|market_education_agent
61|12|كورس صغير مسجل (فيديو) تبيعيه مرة واحدة لعدد غير محدود من العملاء|
62|13|إدارة صفحة Facebook لعميل + الرد على الكومنتات|facebook_agent
63|13|تحليل بروفايل Instagram لعميل محتمل (فرز جودة)|instagram_agent
64|13|اكتشاف ترندات TikTok مناسبة لبيزنس معين|tiktok_agent
65|13|صياغة رسائل تواصل احترافية على LinkedIn لـ B2B|linkedin_agent
66|13|رصد تفاعل على X/Twitter لعلامة تجارية|twitter_agent
67|13|باقة "إدارة 3 منصات" شهرية موحدة — كل الـ social agents مع بعض|
68|14|فحص مخاطر صفقة قبل ما عميلك يوقع عليها|verification_agent
69|14|مراجعة بيانات طرف تاني في صفقة قبل التعامل معاه|verification_agent
70|14|خدمة "تأكد قبل ما تدفع" لمشتري أونلاين قلقانين من النصب|verification_agent
71|15|تدريب فريق مبيعات صغير على الرد على اعتراضات|sales_agent,customer_psychology_agent
72|15|صياغة استراتيجية تفاوض قبل صفقة كبيرة|negotiation_agent
73|15|تحليل سبب خسارة صفقة قديمة|customer_psychology_agent
74|15|اكتشاف إشارات الشراء في محادثة عميل غامضة|customer_psychology_agent
75|15|باقة "زود مبيعاتك 20%" — Upsell/Cross-sell استشاري|upsell_agent
76|16|بيع Leads مؤهلة لشركات تانية بسعر ثابت للـ Lead|research_agent,lead_generation_agent
77|16|باقة "10 عملاء محتملين شهريًا" لبيزنس صغير|research_agent
78|16|فرز عملاء مهتمين فعليًا من قائمة عشوائية|customer_hunter_agent
79|16|تقرير فرص شهري لصاحب بيزنس (Opportunity Report)|research_agent
80|17|نظام تتبع دفعات فودافون كاش لمحلات صغيرة تانية|payment_agent
81|17|خدمة تذكير عملاء بمواعيد الدفع المتأخرة|payment_agent,sales_agent
82|18|تقرير إيرادات شهري جاهز للعرض على مستثمر|revenue_engine
83|18|لوحة متابعة محفظة مشاريع صغيرة (لو عندك أكتر من مصدر دخل)|venture_studio
84|18|تصدير كل بيانات العميل لشيت جاهز|sheets_sync
85|19|عيادات وصالونات: محتوى + حجز + رد على استفسارات|websiteless_business_agent,faq_education_agent
86|19|مطاعم/كافيهات: قوائم طعام + بوستات + عروض|marketing_agent,websiteless_business_agent
87|19|محلات ملابس: كتالوج + محتوى موسمي|websiteless_business_agent,marketing_agent
88|19|عقارات: وصف عقار جذاب + تحليل سعر السوق|marketing_agent,market_competitor_agent
89|19|سياحة/سفر: باقات مخصصة + محتوى ترويجي|marketing_agent,product_builder_agent
90|19|تعليم خاص/دروس: صفحة هبوط + رد على استفسارات أولياء الأمور|websiteless_business_agent,faq_education_agent
91|20|اشتراك شهري "محتوى + رد على العملاء" لتاجر واحد|
92|20|اشتراك "مراقبة المنافسين شهريًا" لعميل|
93|20|اشتراك "تقرير فرص أسبوعي" لصاحب بيزنس|
94|20|اشتراك "إدارة صفحة كاملة" (محتوى + رد + متابعة) شامل|
95|20|باقات متدرجة (أساسية/متوسطة/متقدمة) لنفس الخدمة — سعر مختلف حسب عدد المنصات/البوستات|
'''

INCOME_IDEAS = []
for line in _RAW.strip().splitlines():
    idea_id, category_id, idea, agents = line.split("|", 3)
    INCOME_IDEAS.append({
        "id": int(idea_id),
        "category": CATEGORIES[int(category_id)],
        "idea": idea.strip(),
        "agents": [a.strip() for a in agents.split(",") if a.strip()],
    })


def get_idea(idea_id: int):
    for idea in INCOME_IDEAS:
        if idea["id"] == idea_id:
            return idea
    return None


def search_ideas(query: str = "", category: str = "", limit: int = 10):
    q, c = query.strip().lower(), category.strip().lower()
    results = []
    for idea in INCOME_IDEAS:
        if c and c not in idea["category"].lower():
            continue
        haystack = (idea["idea"] + " " + " ".join(idea["agents"]) + " " + idea["category"]).lower()
        if q and q not in haystack:
            continue
        results.append(idea)
        if len(results) >= max(1, limit):
            break
    return results
