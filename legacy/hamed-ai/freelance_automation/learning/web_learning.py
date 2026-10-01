"""
Web Learning System - نظام التعلم الذاتي من الإنترنت
يتعلم من جميع المصادر المتاحة على الإنترنت
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import re

class WebLearningDB:
    """قاعدة بيانات التعلم من الإنترنت"""
    
    def __init__(self, db_path: str = "web_learning.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول المصادر التعليمية
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                category TEXT,
                content_type TEXT,
                quality_score REAL DEFAULT 0,
                learned_at TEXT,
                last_updated TEXT
            )
        """)
        
        # جدول المعرفة المكتسبة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acquired_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                subtopic TEXT,
                knowledge TEXT NOT NULL,
                source_id INTEGER,
                confidence REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0,
                created_at TEXT,
                FOREIGN KEY (source_id) REFERENCES learning_sources(id)
            )
        """)
        
        # جدول استراتيجيات البيع
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_strategies_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_name TEXT NOT NULL,
                service_type TEXT,
                industry TEXT,
                strategy_details TEXT,
                success_rate REAL DEFAULT 0,
                implementation_steps TEXT,
                tips TEXT,
                source_url TEXT,
                learned_at TEXT
            )
        """)
        
        # جدول اتجاهات السوق
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trend_name TEXT NOT NULL,
                industry TEXT,
                description TEXT,
                opportunity_score REAL DEFAULT 0,
                detected_at TEXT,
                expires_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        # إضافة معرفة افتراضية
        self._add_default_knowledge()
    
    def _add_default_knowledge(self):
        """إضافة معرفة افتراضية شاملة"""
        
        # استراتيجيات البيع الشاملة
        strategies = [
            {
                'name': 'AIDA Model',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج AIDA الكلاسيكي:
1. Attention (الانتباه): اجذب انتباه العميل
2. Interest (الاهتمام): اخلق اهتمامه بالخدمة
3. Desire (الرغبة): اجعله يرغب في الشراء
4. Action (العمل): حثه على اتخاذ قرار الشراء''',
                'steps': '1. عنوان جذاب\n2. مشكلة العميل\n3. الحل المقدم\n4. المميزات\n5. العرض الخاص\n6. دعوة للعمل',
                'tips': 'استخدم عناوين قوية، ركز على الفوائد وليس المميزات، اعرض شهادات العملاء'
            },
            {
                'name': 'SPIN Selling',
                'service_type': 'consulting',
                'industry': 'B2B',
                'details': '''نموذج SPIN للبيع الاستشاري:
1. Situation (الوضع): افهم وضع العميل الحالي
2. Problem (المشكلة): حدد مشاكله
3. Implication (التأثير): أظهر تأثير المشاكل
4. Need-payoff (الحل): قدم الحل المناسب''',
                'steps': '1. اسئلة عن الوضع الحالي\n2. اسئلة عن المشاكل\n3. اسئلة عن التأثير\n4. اسئلة عن الحل المثالي',
                'tips': 'استمع أكثر مما تتكلم، اطرح اسئلة ذكية، قدم حلول مخصصة'
            },
            {
                'name': 'Challenger Sale',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج Challenger Sale:
1. Teach (علم): علم العميل شيئاً جديداً
2. Tailor (خصص): خصص الرسالة حسب العميل
3. Take Control (تحكم): تحكم في عملية البيع''',
                'steps': '1. قدم رؤية جديدة\n2. تحدى افتراضات العميل\n3. قدم حلاً فريداً\n4. أغلق الصفقة',
                'tips': 'كن واثقاً، قدم قيمة حقيقية، لا تخف من التحدي'
            },
            {
                'name': 'Solution Selling',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج Solution Selling:
1. حدد مشكلة العميل
2. قدم حلاً شاملاً
3. أظهر القيمة المضافة
4. قدم دليلاً على النجاح''',
                'steps': '1. تحليل الاحتياجات\n2. تصميم الحل\n3. عرض القيمة\n4. إثبات النجاح',
                'tips': 'ركز على حل المشكلة، قدم حالات نجاح، كن شريكاً وليس بائعاً'
            },
            {
                'name': 'Value-Based Selling',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج Value-Based Selling:
1. حدد القيمة للعميل
2. كم القيمة مالياً
3. أظهر العائد على الاستثمار
4. قدم العرض بناءً على القيمة''',
                'steps': '1. تحليل القيمة\n2. حساب العائد\n3. عرض الفوائد\n4. تقديم العرض',
                'tips': 'ركز على العائد على الاستثمار، استخدم أرقام حقيقية، قدم ضمانات'
            },
            {
                'name': 'Social Selling',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج Social Selling:
1. بناء العلاقات على السوشيال ميديا
2. تقديم قيمة مجانية
3. بناء الثقة
4. التحويل إلى عملاء''',
                'steps': '1. بناء الملف الشخصي\n2. نشر محتوى قيم\n3. التفاعل مع المتابعين\n4. بناء العلاقات\n5. التحويل',
                'tips': 'كن أصلياً، قدم قيمة أولاً، ابنِ علاقات حقيقية'
            },
            {
                'name': 'Consultative Selling',
                'service_type': 'consulting',
                'industry': 'all',
                'details': '''نموذج Consultative Selling:
1. كن مستشاراً وليس بائعاً
2. افهم احتياجات العميل بعمق
3. قدم نصائح قيمة
4. اقترح الحلول المناسبة''',
                'steps': '1. الاستماع النشط\n2. طرح اسئلة ذكية\n3. تقديم نصائح\n4. اقتراح الحلول',
                'tips': 'كن صادقاً، قدم قيمة حقيقية، ابنِ ثقة طويلة المدى'
            },
            {
                'name': 'Relationship Selling',
                'service_type': 'all',
                'industry': 'all',
                'details': '''نموذج Relationship Selling:
1. بناء علاقات طويلة المدى
2. التركيز على رضا العميل
3. المتابعة المستمرة
4. بناء الولاء''',
                'steps': '1. التعرف على العميل\n2. بناء الثقة\n3. تقديم خدمة ممتازة\n4. المتابعة',
                'tips': 'العميل السعيد يأتي بعملاء جدد، الاستثمار في العلاقات مربح'
            }
        ]
        
        # معرفة عامة عن البيع
        general_knowledge = [
            {
                'topic': 'علم نفس العميل',
                'subtopic': 'مبادئ التأثير',
                'knowledge': '''مبادئ التأثير الستة (Robert Cialdini):
1. المعاملة بالمثل: قدم شيئاً المجاني أولاً
2. الالتزام والاتساق: احصل على التزام صغير أولاً
3. الدليل الاجتماعي: أظهر أن الآخرين يشترون
4. السلطة: أظهر خبرتك ومصداقيتك
5. الإعجاب: كن ودوداً ومشابهاً للعميل
6. الندرة: اعرض العرض المحدود''',
                'confidence': 0.95
            },
            {
                'topic': 'علم نفس العميل',
                'subtopic': 'أنماط الشخصيات',
                'knowledge': '''أنماط شخصيات العملاء:
1. التحليلي: يحب التفاصيل والأرقام
2. الودود: يحب العلاقات والتفاعل
3. القائد: يحب السرعة والنتائج
4. التعبيري: يحب الإبداع والابتكار

كيف تتعامل مع كل نوع:
- التحليلي: قدم بيانات وإحصائيات
- الودود: ابنِ علاقة شخصية
- القائد: كن مباشراً وسريعاً
- التعبيري: استخدم الإبداع والصور''',
                'confidence': 0.90
            },
            {
                'topic': 'تقنيات البيع',
                'subtopic': 'التعامل مع الاعتراضات',
                'knowledge': '''تقنيات التعامل مع الاعتراضات:
1. استمع بالكامل
2. أظهر التفهم
3. أعد صياغة الاعتراض
4. قدم الحل
5. تأكد من الرضا

اعتراضات شائعة وحلولها:
- "غالي جداً": أظهر القيمة والعائد
- "محتاج أفكر": قدم عرض محدود الوقت
- "عندي مورد تاني": أظهر ما يميزك
- "مش وقت مناسب": أظهر تكلفة التأخير''',
                'confidence': 0.92
            },
            {
                'topic': 'تقنيات البيع',
                'subtopic': 'إغلاق الصفقات',
                'knowledge': '''تقنيات إغلاق الصفقات:
1. الإغلاق المباشر: "هل تريد البدء الآن؟"
2. الإغلاق البديل: "تفضل الخيار أ أم ب؟"
3. الإغلاق بالندرة: "العرض ينتهي غداً"
4. الإغلاق بالتلخيص: "إذاً سنقدم لك..."
5. الإغلاق بالاختبار: "هل هناك أي مانع؟"

علامات الاستعداد للشراء:
- يسأل عن التفاصيل
- يسأل عن السعر
- يسأل عن الدفع
- يتخيل نفسه يستخدم الخدمة''',
                'confidence': 0.88
            },
            {
                'topic': 'التسعير',
                'subtopic': 'استراتيجيات التسعير',
                'knowledge': '''استراتيجيات التسعير:
1. التسعير على أساس القيمة: سعّر حسب القيمة المقدمة
2. التسعير التنافسي: سعّر حسب المنافسين
3. التسعير النفسي: استخدم أرقام مثل 99 بدلاً من 100
4. التسعير الحزمي: قدم حزم بأسعار مختلفة
5. التسعير الديناميكي: غير السعر حسب الطلب

نصائح:
- لا تكن الأرخص دائماً
- قدم قيمة حقيقية
- اعرض خيارات متعددة
- استخدم الخصم بحكمة''',
                'confidence': 0.85
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # إضافة استراتيجيات البيع
        for strategy in strategies:
            cursor.execute("""
                INSERT OR IGNORE INTO sales_strategies_db 
                (strategy_name, service_type, industry, strategy_details, 
                 implementation_steps, tips, learned_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (strategy['name'], strategy['service_type'], strategy['industry'],
                  strategy['details'], strategy['steps'], strategy['tips'],
                  datetime.now().isoformat()))
        
        # إضافة المعرفة العامة
        for knowledge in general_knowledge:
            cursor.execute("""
                INSERT INTO acquired_knowledge 
                (topic, subtopic, knowledge, confidence, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (knowledge['topic'], knowledge['subtopic'], knowledge['knowledge'],
                  knowledge['confidence'], datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def learn_from_url(self, url: str, content: Dict) -> bool:
        """التعلم من URL معين"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # حفظ المصدر
            cursor.execute("""
                INSERT OR REPLACE INTO learning_sources 
                (url, title, category, content_type, quality_score, learned_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (url, content.get('title'), content.get('category'),
                  content.get('content_type'), content.get('quality_score', 0),
                  datetime.now().isoformat()))
            
            source_id = cursor.lastrowid
            
            # حفظ المعرفة المستخرجة
            for item in content.get('knowledge_items', []):
                cursor.execute("""
                    INSERT INTO acquired_knowledge 
                    (topic, subtopic, knowledge, source_id, confidence, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (item['topic'], item.get('subtopic'), item['knowledge'],
                      source_id, item.get('confidence', 0.5),
                      datetime.now().isoformat()))
            
            conn.commit()
            return True
        
        except Exception as e:
            print(f"Error learning from {url}: {e}")
            return False
        
        finally:
            conn.close()
    
    def get_sales_strategy(self, strategy_name: str = None, service_type: str = None) -> List[Dict]:
        """الحصول على استراتيجيات البيع"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM sales_strategies_db WHERE 1=1"
        params = []
        
        if strategy_name:
            query += " AND strategy_name = ?"
            params.append(strategy_name)
        
        if service_type:
            query += " AND (service_type = ? OR service_type = 'all')"
            params.append(service_type)
        
        query += " ORDER BY success_rate DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        strategies = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return strategies
    
    def get_knowledge(self, topic: str = None) -> List[Dict]:
        """الحصول على المعرفة المكتسبة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic:
            cursor.execute("""
                SELECT * FROM acquired_knowledge 
                WHERE topic = ? OR topic LIKE ?
                ORDER BY confidence DESC, usage_count DESC
            """, (topic, f'%{topic}%'))
        else:
            cursor.execute("""
                SELECT * FROM acquired_knowledge 
                ORDER BY confidence DESC, usage_count DESC
            """)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        knowledge = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return knowledge
    
    def get_all_strategies_summary(self) -> Dict:
        """ملخص جميع الاستراتيجيات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sales_strategies_db")
        total_strategies = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM acquired_knowledge")
        total_knowledge = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM learning_sources")
        total_sources = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(confidence) FROM acquired_knowledge")
        avg_confidence = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_strategies': total_strategies,
            'total_knowledge': total_knowledge,
            'total_sources': total_sources,
            'avg_confidence': avg_confidence
        }
