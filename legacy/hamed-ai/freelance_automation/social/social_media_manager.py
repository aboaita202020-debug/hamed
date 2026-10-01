"""
Social Media Manager - نظام إدارة السوشيال ميديا التلقائي
ينشئ المحتوى وينشره ويكبر الصفحات تلقائياً
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class SocialMediaDB:
    """قاعدة بيانات إدارة السوشيال ميديا"""
    
    def __init__(self, db_path: str = "social_media.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الحسابات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                account_name TEXT NOT NULL,
                account_id TEXT,
                followers_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                api_credentials TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT,
                last_synced TEXT
            )
        """)
        
        # جدول المنشورات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                media_urls TEXT,
                hashtags TEXT,
                scheduled_at TEXT,
                published_at TEXT,
                status TEXT DEFAULT 'draft',
                likes_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                shares_count INTEGER DEFAULT 0,
                reach_count INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                FOREIGN KEY (account_id) REFERENCES social_accounts(id)
            )
        """)
        
        # جدول المحتوى المقترح
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                template TEXT,
                best_time_to_post TEXT,
                success_rate REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        
        # جدول النمو
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS growth_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                date TEXT NOT NULL,
                followers_count INTEGER,
                following_count INTEGER,
                posts_count INTEGER,
                engagement_rate REAL,
                new_followers INTEGER DEFAULT 0,
                lost_followers INTEGER DEFAULT 0,
                FOREIGN KEY (account_id) REFERENCES social_accounts(id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # إضافة أفكار محتوى افتراضية
        self._add_default_content_ideas()
    
    def _add_default_content_ideas(self):
        """إضافة أفكار محتوى افتراضية"""
        ideas = [
            {
                'category': 'educational',
                'content_type': 'carousel',
                'title': 'نصائح احترافية',
                'description': 'مشاركة نصائح قيمة في مجالك',
                'template': '''💡 نصيحة اليوم:

{tip_title}

{tip_content}

✅ طبق هذه النصيحة وشاركنا النتيجة!

#نصائح #تطوير #احتراف''',
                'best_time_to_post': '10:00 AM'
            },
            {
                'category': 'promotional',
                'content_type': 'image',
                'title': 'عرض خاص',
                'description': 'الترويج للعروض والخدمات',
                'template': '''🎉 عرض خاص لفترة محدودة!

{service_name}

💰 السعر: {price}
⏱️ العرض ينتهي: {deadline}

✅ مميزات الخدمة:
{features}

📞 للتواصل: 01061245527

#عروض #خدمات #خصم''',
                'best_time_to_post': '2:00 PM'
            },
            {
                'category': 'engagement',
                'content_type': 'poll',
                'title': 'استطلاع رأي',
                'description': 'زيادة التفاعل مع المتابعين',
                'template': '''🤔 سؤال اليوم:

{question}

🔘 الخيار الأول
🔘 الخيار الثاني
🔘 الخيار الثالث

شاركنا رأيك في التعليقات! 👇

#استطلاع #تفاعل''',
                'best_time_to_post': '6:00 PM'
            },
            {
                'category': 'testimonial',
                'content_type': 'image',
                'title': 'شهادة عميل',
                'description': 'نشر شهادات العملاء السعداء',
                'template': '''⭐ شهادة عميل سعيد:

"{testimonial}"

- {client_name}
{client_position}

🎯 النتيجة: {result}

شكراً لثقتك بنا! 🙏

#شهادات #عملاء #نجاح''',
                'best_time_to_post': '11:00 AM'
            },
            {
                'category': 'behind_scenes',
                'content_type': 'video',
                'title': 'وراء الكواليس',
                'description': 'إظهار العمل خلف الكواليس',
                'template': '''🎬 وراء الكواليس:

شوف كيف بنشتغل على {project_name}!

{description}

✅ الجودة أولاً
✅ الالتزام بالمواعيد
✅ رضا العملاء

#وراء_الكواليس #عمل #فريق''',
                'best_time_to_post': '3:00 PM'
            },
            {
                'category': 'tips',
                'content_type': 'reel',
                'title': 'نصيحة سريعة',
                'description': 'فيديو قصير بنصيحة قيمة',
                'template': '''⚡ نصيحة سريعة في 30 ثانية:

{tip}

✅ جربها وشاركنا النتيجة!

#نصائح_سريعة #تطوير #فيديو''',
                'best_time_to_post': '5:00 PM'
            },
            {
                'category': 'case_study',
                'content_type': 'carousel',
                'title': 'دراسة حالة',
                'description': 'عرض حالات نجاح مفصلة',
                'template': '''📊 دراسة حالة:

العميل: {client_name}
التحدي: {challenge}
الحل: {solution}

📈 النتائج:
{results}

💡 الدروس المستفادة:
{lessons}

#دراسة_حالة #نجاح #نتائج''',
                'best_time_to_post': '9:00 AM'
            },
            {
                'category': 'industry_news',
                'content_type': 'text',
                'title': 'أخبار الصناعة',
                'description': 'مشاركة أخبار وتطورات المجال',
                'template': '''📰 خبر مهم في {industry}:

{news_title}

{news_summary}

💡 رأيي:
{opinion}

ما رأيكم؟ شاركونا في التعليقات! 👇

#أخبار #تطورات #صناعة''',
                'best_time_to_post': '8:00 AM'
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for idea in ideas:
            cursor.execute("""
                INSERT INTO content_ideas 
                (category, content_type, title, description, template, best_time_to_post, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (idea['category'], idea['content_type'], idea['title'],
                  idea['description'], idea['template'], idea['best_time_to_post'],
                  datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def add_account(self, platform: str, account_name: str, account_id: str = None) -> int:
        """إضافة حساب سوشيال ميديا"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO social_accounts 
            (platform, account_name, account_id, created_at)
            VALUES (?, ?, ?, ?)
        """, (platform, account_name, account_id, datetime.now().isoformat()))
        
        account_db_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return account_db_id
    
    def create_post(self, account_id: int, platform: str, content: str,
                   hashtags: str = None, scheduled_at: str = None) -> int:
        """إنشاء منشور جديد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO social_posts 
            (account_id, platform, content, hashtags, scheduled_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (account_id, platform, content, hashtags, scheduled_at,
              'scheduled' if scheduled_at else 'draft'))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def generate_content(self, category: str = None, platform: str = None) -> Dict:
        """توليد محتوى تلقائي"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM content_ideas 
                WHERE category = ?
                ORDER BY success_rate DESC, RANDOM()
                LIMIT 1
            """, (category,))
        else:
            cursor.execute("""
                SELECT * FROM content_ideas 
                ORDER BY success_rate DESC, RANDOM()
                LIMIT 1
            """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            idea = dict(zip(columns, row))
            
            # توليد محتوى من القالب
            content = self._fill_template(idea['template'], category)
            
            return {
                'idea': idea,
                'generated_content': content,
                'best_time': idea['best_time_to_post']
            }
        
        return None
    
    def _fill_template(self, template: str, category: str) -> str:
        """ملء القالب بمحتوى حقيقي"""
        # هنا يمكن استخدام AI لتوليد محتوى حقيقي
        # حالياً نعيد القالب كما هو
        
        # أمثلة على المحتوى الحقيقي حسب الفئة
        examples = {
            'educational': {
                'tip_title': 'كيف تختار أفضل خدمة لاحتياجاتك',
                'tip_content': 'ابحث عن الجودة وليس السعر فقط. الخدمة الرخيصة قد تكلفك أكثر على المدى الطويل.'
            },
            'promotional': {
                'service_name': 'تحليل المواقع الاحترافي',
                'price': '$50',
                'deadline': 'نهاية الشهر',
                'features': '- تحليل شامل\n- تقرير مفصل\n- توصيات عملية'
            },
            'engagement': {
                'question': 'ما هي أكبر تحدي تواجهه في مشروعك الحالي؟'
            }
        }
        
        # ملء القالب بالبيانات
        if category in examples:
            for key, value in examples[category].items():
                template = template.replace(f'{{{key}}}', str(value))
        
        return template
    
    def get_content_ideas(self, category: str = None) -> List[Dict]:
        """الحصول على أفكار المحتوى"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM content_ideas WHERE category = ?
                ORDER BY success_rate DESC
            """, (category,))
        else:
            cursor.execute("""
                SELECT * FROM content_ideas 
                ORDER BY success_rate DESC
            """)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        ideas = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return ideas
    
    def record_growth(self, account_id: int, followers: int, following: int,
                     posts: int, engagement_rate: float):
        """تسجيل بيانات النمو"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # الحصول على البيانات السابقة
        cursor.execute("""
            SELECT followers_count FROM growth_metrics 
            WHERE account_id = ? 
            ORDER BY date DESC LIMIT 1
        """, (account_id,))
        
        result = cursor.fetchone()
        previous_followers = result[0] if result else 0
        
        new_followers = max(0, followers - previous_followers)
        lost_followers = max(0, previous_followers - followers)
        
        cursor.execute("""
            INSERT INTO growth_metrics 
            (account_id, date, followers_count, following_count, posts_count,
             engagement_rate, new_followers, lost_followers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (account_id, datetime.now().strftime('%Y-%m-%d'), followers,
              following, posts, engagement_rate, new_followers, lost_followers))
        
        # تحديث الحساب
        cursor.execute("""
            UPDATE social_accounts 
            SET followers_count = ?, following_count = ?, posts_count = ?,
                engagement_rate = ?, last_synced = ?
            WHERE id = ?
        """, (followers, following, posts, engagement_rate,
              datetime.now().isoformat(), account_id))
        
        conn.commit()
        conn.close()
    
    def get_accounts_summary(self) -> List[Dict]:
        """ملخص جميع الحسابات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM social_accounts 
            WHERE is_active = 1
            ORDER BY followers_count DESC
        """)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        accounts = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return accounts
