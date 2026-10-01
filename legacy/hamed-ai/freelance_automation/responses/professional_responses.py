"""
Professional Response System - نظام الردود الاحترافية
ردود احترافية عبر واتساب وتيليجرام باللهجة المصرية
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class ProfessionalResponseDB:
    """قاعدة بيانات الردود الاحترافية"""
    
    def __init__(self, db_path: str = "professional_responses.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الردود الاحترافية
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professional_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT NOT NULL,
                service_type TEXT,
                response_template TEXT NOT NULL,
                tone TEXT DEFAULT 'professional',
                language TEXT DEFAULT 'arabic_egyptian',
                success_rate REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        
        # جدول المحادثات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                platform TEXT,
                message TEXT,
                response TEXT,
                intent_detected TEXT,
                outcome TEXT,
                created_at TEXT
            )
        """)
        
        # جدول الخدمات المتاحة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS available_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT UNIQUE NOT NULL,
                description TEXT,
                base_price REAL,
                delivery_time TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
        
        # إضافة الردود الاحترافية الافتراضية
        self._add_default_responses()
    
    def _add_default_responses(self):
        """إضافة الردود الاحترافية الافتراضية"""
        responses = [
            {
                'intent': 'greeting',
                'service_type': None,
                'response_template': '''أهلاً وسهلاً بك! 👋

يسعدنا تواصلك معنا. نحن هنا لمساعدتك في تحقيق أهدافك الرقمية.

كيف يمكننا خدمتك اليوم؟''',
                'tone': 'professional'
            },
            {
                'intent': 'service_inquiry',
                'service_type': 'website_analysis',
                'response_template': '''شكراً لاهتمامك بخدمتنا! 🎯

نقدم خدمة تحليل المواقع الاحترافية التي تشمل:

✅ تحليل شامل لأداء الموقع
✅ تقييم سرعة التحميل
✅ تحليل SEO
✅ تقييم تجربة المستخدم
✅ تقرير مفصل مع التوصيات

💰 السعر: يبدأ من $50
⏱️ مدة التسليم: 2-3 أيام عمل

هل تود البدء بتحليل موقعك؟ يرجى إرسال الرابط.''',
                'tone': 'professional'
            },
            {
                'intent': 'service_inquiry',
                'service_type': 'seo_optimization',
                'response_template': '''شكراً لاهتمامك بخدماتنا! 📈

نقدم خدمة تحسين محركات البحث (SEO) الاحترافية:

✅ تحليل شامل للموقع
✅ تحسين الكلمات المفتاحية
✅ تحسين المحتوى
✅ بناء روابط خلفية
✅ تقارير شهرية مفصلة

💰 السعر: يبدأ من $150
⏱️ مدة التسليم: 30 يوم
📊 النتائج المتوقعة: زيادة الزيارات 150-300%

هل تود الحصول على استشارة مجانية؟''',
                'tone': 'professional'
            },
            {
                'intent': 'service_inquiry',
                'service_type': 'content_writing',
                'response_template': '''شكراً لاهتمامك بخدماتنا! ✍️

نقدم خدمة كتابة المحتوى الاحترافي:

✅ مقالات SEO احترافية
✅ محتوى مواقع إلكترونية
✅ منشورات سوشيال ميديا
✅ وصف منتجات
✅ محتوى تسويقي

💰 الأسعار:
- مقال 500 كلمة: $15
- مقال 1000 كلمة: $25
- محتوى موقع كامل: حسب المشروع

⏱️ مدة التسليم: حسب حجم المشروع

هل تود الاطلاع على عينات من أعمالنا؟''',
                'tone': 'professional'
            },
            {
                'intent': 'service_inquiry',
                'service_type': 'custom',
                'response_template': '''شكراً لاهتمامك بخدماتنا! 🎯

نحن نقدم حلولاً مخصصة تناسب احتياجاتك الخاصة.

يمكننا مساعدتك في:
✅ تطوير المواقع والتطبيقات
✅ التسويق الرقمي
✅ تصميم الجرافيك
✅ إنتاج الفيديو
✅ أي خدمة رقمية أخرى

يرجى إخبارنا بتفاصيل احتياجاتك، وسنقدم لك عرضاً مخصصاً.

💬 نحن هنا لخدمتك!''',
                'tone': 'professional'
            },
            {
                'intent': 'price_inquiry',
                'service_type': None,
                'response_template': '''شكراً لسؤالك! 💰

أسعارنا تنافسية وتعكس جودة الخدمة المقدمة:

📊 تحليل المواقع: يبدأ من $50
📈 تحسين SEO: يبدأ من $150
✍️ كتابة المحتوى: يبدأ من $15/مقال
🎨 التصميم: يبدأ من $30
📱 إدارة السوشيال ميديا: يبدأ من $200/شهر

💎 نقدم خصومات خاصة للطلبات الكبيرة
🎁 استشارة مجانية للعملاء الجدد

هل تود معرفة تفاصيل أكثر عن خدمة معينة؟''',
                'tone': 'professional'
            },
            {
                'intent': 'payment_inquiry',
                'service_type': None,
                'response_template': '''شكراً لاهتمامك! 💳

نوفر طرق دفع متعددة لراحتك:

📱 فودافون كاش: 01061245527
💳 تحويل بنكي
🏦 PayPal (للعملاء الدوليين)

📋 عملية الدفع:
1. تأكيد الطلب
2. إرسال تفاصيل الدفع
3. تأكيد الاستلام
4. بدء العمل

✅ نضمن لك الأمان والشفافية في كل خطوة

هل تود إتمام عملية الدفع؟''',
                'tone': 'professional'
            },
            {
                'intent': 'delivery_inquiry',
                'service_type': None,
                'response_template': '''شكراً لسؤالك! ⏱️

مواعيد التسليم تعتمد على نوع الخدمة:

📊 تحليل المواقع: 2-3 أيام عمل
📈 تحسين SEO: 30 يوم
✍️ كتابة المحتوى: 3-7 أيام (حسب الحجم)
🎨 التصميم: 3-5 أيام
📱 إدارة السوشيال ميديا: مستمر

✅ نلتزم بالمواعيد المحددة
🔄 تحديثات دورية أثناء العمل
📞 دعم مستمر بعد التسليم

هل لديك موعد محدد تحتاج الالتزام به؟''',
                'tone': 'professional'
            },
            {
                'intent': 'complaint',
                'service_type': None,
                'response_template': '''نعتذر بشدة عن أي إزعاج! 🙏

نحن نقدر ملاحظاتك ونأخذها على محمل الجد.

📞 يرجى إخبارنا بتفاصيل المشكلة:
- ما الذي حدث؟
- متى حدث؟
- كيف يمكننا المساعدة؟

✅ سنتعامل مع مشكلتك فوراً
🔄 سنقدم حلاً مناسباً
💎 رضاك أولويتنا القصوى

نحن هنا لخدمتك وحل أي مشكلة تواجهك.''',
                'tone': 'empathetic'
            },
            {
                'intent': 'thank_you',
                'service_type': None,
                'response_template': '''شكراً لك! 🙏

يسعدنا خدمتك ونتمنى أن نكون عند حسن ظنك.

💎 نحن هنا دائماً لخدمتك
📞 لا تتردد في التواصل معنا لأي استفسار
⭐ رضاك هو هدفنا

نتطلع للتعاون معك مرة أخرى!''',
                'tone': 'professional'
            },
            {
                'intent': 'unknown_service',
                'service_type': None,
                'response_template': '''شكراً لاهتمامك! 🎯

نحن نقدم مجموعة واسعة من الخدمات الرقمية، وإذا كانت خدمتك غير مدرجة في قائمتنا، يمكننا:

✅ تقديم حل مخصص لاحتياجاتك
✅ التوصية بشركائنا الموثوقين
✅ البحث عن أفضل حل لك

يرجى إخبارنا بتفاصيل ما تحتاجه، وسنبذل قصارى جهدنا لمساعدتك.

💬 نحن هنا لخدمتك!''',
                'tone': 'professional'
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for response in responses:
            cursor.execute("""
                INSERT OR IGNORE INTO professional_responses 
                (intent, service_type, response_template, tone, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (response['intent'], response['service_type'], 
                  response['response_template'], response['tone'],
                  datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_response(self, intent: str, service_type: str = None) -> Optional[str]:
        """الحصول على رد احترافي"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if service_type:
            cursor.execute("""
                SELECT response_template FROM professional_responses
                WHERE intent = ? AND service_type = ?
                ORDER BY success_rate DESC, usage_count DESC
                LIMIT 1
            """, (intent, service_type))
        else:
            cursor.execute("""
                SELECT response_template FROM professional_responses
                WHERE intent = ? AND service_type IS NULL
                ORDER BY success_rate DESC, usage_count DESC
                LIMIT 1
            """, (intent,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def record_conversation(self, client_id: str, platform: str,
                           message: str, response: str,
                           intent_detected: str, outcome: str):
        """تسجيل المحادثة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations 
            (client_id, platform, message, response, intent_detected, outcome, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (client_id, platform, message, response, intent_detected,
              outcome, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def update_response_stats(self, response_id: int, success: bool):
        """تحديث إحصائيات الرد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT usage_count, success_rate FROM professional_responses
            WHERE id = ?
        """, (response_id,))
        
        result = cursor.fetchone()
        if result:
            usage_count, current_rate = result
            new_usage = usage_count + 1
            
            if success:
                new_rate = ((current_rate * usage_count) + 100) / new_usage
            else:
                new_rate = (current_rate * usage_count) / new_usage
            
            cursor.execute("""
                UPDATE professional_responses
                SET usage_count = ?, success_rate = ?
                WHERE id = ?
            """, (new_usage, new_rate, response_id))
            
            conn.commit()
        
        conn.close()
