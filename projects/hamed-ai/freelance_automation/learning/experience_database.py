"""
Experience Database - قاعدة بيانات التعلم من التجارب
تخزن كل تجربة (نجاح/فشل) وتستعلم منها لتحسين القرارات
"""
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.logger import logger

class ExperienceDatabase:
    """قاعدة بيانات التعلم من التجارب"""
    
    def __init__(self, db_path: str = "data/experiences.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"ExperienceDatabase initialized at {db_path}")
    
    def _get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # جدول التجارب الرئيسية
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experience_type TEXT NOT NULL,
                category TEXT NOT NULL,
                input_data TEXT NOT NULL,
                decision TEXT NOT NULL,
                outcome TEXT NOT NULL,
                success INTEGER NOT NULL,
                revenue REAL,
                loss REAL,
                lessons_learned TEXT,
                confidence_score REAL,
                time_spent REAL,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        """)
        
        # جدول أنماط النجاح
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS success_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                success_rate REAL NOT NULL,
                occurrence_count INTEGER NOT NULL,
                last_seen TEXT NOT NULL,
                confidence REAL NOT NULL
            )
        """)
        
        # جدول الأخطاء والدروس
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mistake_type TEXT NOT NULL,
                description TEXT NOT NULL,
                context TEXT NOT NULL,
                lesson TEXT NOT NULL,
                severity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # جدول تحليلات المواقع
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                domain TEXT NOT NULL,
                site_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                issues_found TEXT,
                recommendations TEXT,
                message_sent INTEGER DEFAULT 0,
                response_received INTEGER DEFAULT 0,
                converted_to_client INTEGER DEFAULT 0,
                revenue_generated REAL DEFAULT 0,
                analyzed_at TEXT NOT NULL
            )
        """)
        
        # جدول رسائل العملاء
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_url TEXT NOT NULL,
                message_template TEXT NOT NULL,
                message_sent TEXT NOT NULL,
                response_type TEXT,
                response_content TEXT,
                outcome TEXT,
                conversion_rate REAL,
                sent_at TEXT NOT NULL,
                responded_at TEXT
            )
        """)
        
        # جدول قرارات الشراء
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                supplier TEXT NOT NULL,
                price REAL NOT NULL,
                quality_score REAL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                actual_outcome TEXT,
                profit_loss REAL,
                created_at TEXT NOT NULL
            )
        """)
        
        # جدول مفاوضات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS negotiations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_type TEXT NOT NULL,
                party_name TEXT NOT NULL,
                initial_offer REAL,
                counter_offers TEXT,
                final_deal REAL,
                strategy_used TEXT,
                success INTEGER,
                lessons TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ==================== تسجيل التجارب ====================
    
    def record_experience(self, 
                         experience_type: str,
                         category: str,
                         input_data: Dict,
                         decision: str,
                         outcome: str,
                         success: bool,
                         revenue: float = 0,
                         loss: float = 0,
                         lessons: str = "",
                         confidence: float = 0.5,
                         time_spent: float = 0) -> int:
        """تسجيل تجربة جديدة"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO experiences 
            (experience_type, category, input_data, decision, outcome, 
             success, revenue, loss, lessons_learned, confidence_score, 
             time_spent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            experience_type,
            category,
            json.dumps(input_data, ensure_ascii=False),
            decision,
            outcome,
            1 if success else 0,
            revenue,
            loss,
            lessons,
            confidence,
            time_spent,
            datetime.now().isoformat()
        ))
        
        experience_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # تحديث أنماط النجاح
        if success:
            self._update_success_pattern(category, input_data)
        
        logger.info(f"Experience recorded: {experience_type} - {'SUCCESS' if success else 'FAILURE'}")
        return experience_id
    
    def record_site_analysis(self,
                            url: str,
                            domain: str,
                            site_type: str,
                            score: int,
                            issues: List[str],
                            recommendations: List[str],
                            message_sent: bool = False,
                            response_received: bool = False,
                            converted: bool = False,
                            revenue: float = 0) -> int:
        """تسجيل تحليل موقع"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO site_analyses
            (url, domain, site_type, score, issues_found, recommendations,
             message_sent, response_received, converted_to_client, revenue_generated, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            url, domain, site_type, score,
            json.dumps(issues, ensure_ascii=False),
            json.dumps(recommendations, ensure_ascii=False),
            1 if message_sent else 0,
            1 if response_received else 0,
            1 if converted else 0,
            revenue,
            datetime.now().isoformat()
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    
    def record_client_message(self,
                             site_url: str,
                             template: str,
                             message: str,
                             response_type: str = None,
                             response: str = None,
                             outcome: str = None,
                             conversion_rate: float = 0) -> int:
        """تسجيل رسالة عميل"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO client_messages
            (site_url, message_template, message_sent, response_type, 
             response_content, outcome, conversion_rate, sent_at, responded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            site_url, template, message,
            response_type, response, outcome, conversion_rate,
            datetime.now().isoformat(),
            datetime.now().isoformat() if response else None
        ))
        
        msg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return msg_id
    
    def record_purchase_decision(self,
                                product: str,
                                supplier: str,
                                price: float,
                                quality: float,
                                decision: str,
                                reason: str,
                                actual_outcome: str = None,
                                profit_loss: float = 0) -> int:
        """تسجيل قرار شراء"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO purchase_decisions
            (product, supplier, price, quality_score, decision, reason,
             actual_outcome, profit_loss, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product, supplier, price, quality, decision, reason,
            actual_outcome, profit_loss, datetime.now().isoformat()
        ))
        
        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return decision_id
    
    def record_negotiation(self,
                          party_type: str,
                          party_name: str,
                          initial_offer: float,
                          counter_offers: List[float],
                          final_deal: float,
                          strategy: str,
                          success: bool,
                          lessons: str = "") -> int:
        """تسجيل عملية تفاوض"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO negotiations
            (party_type, party_name, initial_offer, counter_offers,
             final_deal, strategy_used, success, lessons, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            party_type, party_name, initial_offer,
            json.dumps(counter_offers),
            final_deal, strategy,
            1 if success else 0,
            lessons,
            datetime.now().isoformat()
        ))
        
        neg_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return neg_id
    
    def record_mistake(self,
                      mistake_type: str,
                      description: str,
                      context: Dict,
                      lesson: str,
                      severity: str = "medium") -> int:
        """تسجيل خطأ والتعلم منه"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO mistakes
            (mistake_type, description, context, lesson, severity, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            mistake_type, description,
            json.dumps(context, ensure_ascii=False),
            lesson, severity,
            datetime.now().isoformat()
        ))
        
        mistake_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return mistake_id
    
    # ==================== الاستعلام من التجارب ====================
    
    def get_similar_experiences(self, 
                               category: str,
                               input_data: Dict,
                               limit: int = 10) -> List[Dict]:
        """الحصول على تجارب مشابهة"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM experiences
            WHERE category = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (category, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_success_rate(self, category: str, days: int = 30) -> Dict:
        """حساب معدل النجاح في فئة معينة"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(success) as successful,
                AVG(confidence_score) as avg_confidence,
                SUM(revenue) as total_revenue,
                SUM(loss) as total_loss
            FROM experiences
            WHERE category = ? AND created_at >= ?
        """, (category, since))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row or row['total'] == 0:
            return {
                'total': 0,
                'successful': 0,
                'success_rate': 0,
                'avg_confidence': 0,
                'total_revenue': 0,
                'total_loss': 0,
                'net_profit': 0
            }
        
        return {
            'total': row['total'],
            'successful': row['successful'] or 0,
            'success_rate': (row['successful'] or 0) / row['total'] * 100,
            'avg_confidence': row['avg_confidence'] or 0,
            'total_revenue': row['total_revenue'] or 0,
            'total_loss': row['total_loss'] or 0,
            'net_profit': (row['total_revenue'] or 0) - (row['total_loss'] or 0)
        }
    
    def get_best_strategies(self, category: str, limit: int = 5) -> List[Dict]:
        """الحصول على أفضل الاستراتيجيات من التجارب"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                decision,
                COUNT(*) as usage_count,
                SUM(success) as success_count,
                AVG(revenue) as avg_revenue,
                SUM(revenue) as total_revenue
            FROM experiences
            WHERE category = ? AND success = 1
            GROUP BY decision
            ORDER BY success_count DESC, avg_revenue DESC
            LIMIT ?
        """, (category, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_site_analysis_stats(self) -> Dict:
        """إحصائيات تحليل المواقع"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_analyses,
                SUM(message_sent) as messages_sent,
                SUM(response_received) as responses_received,
                SUM(converted_to_client) as conversions,
                SUM(revenue_generated) as total_revenue,
                AVG(score) as avg_score
            FROM site_analyses
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        total = row['total_analyses'] or 0
        messages = row['messages_sent'] or 0
        responses = row['response_received'] or 0
        conversions = row['conversions'] or 0
        
        return {
            'total_analyses': total,
            'messages_sent': messages,
            'responses_received': responses,
            'response_rate': (responses / messages * 100) if messages > 0 else 0,
            'conversions': conversions,
            'conversion_rate': (conversions / messages * 100) if messages > 0 else 0,
            'total_revenue': row['total_revenue'] or 0,
            'avg_score': row['avg_score'] or 0
        }
    
    def get_message_effectiveness(self, limit: int = 10) -> List[Dict]:
        """تحليل فعالية الرسائل"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                message_template,
                COUNT(*) as times_used,
                SUM(CASE WHEN response_type IS NOT NULL THEN 1 ELSE 0 END) as responses,
                SUM(CASE WHEN outcome = 'converted' THEN 1 ELSE 0 END) as conversions,
                AVG(conversion_rate) as avg_conversion_rate
            FROM client_messages
            GROUP BY message_template
            ORDER BY conversions DESC, avg_conversion_rate DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_purchase_insights(self) -> Dict:
        """رؤى من قرارات الشراء"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_decisions,
                SUM(CASE WHEN decision = 'approved' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN decision = 'rejected' THEN 1 ELSE 0 END) as rejected,
                AVG(profit_loss) as avg_profit,
                SUM(profit_loss) as total_profit
            FROM purchase_decisions
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_decisions': row['total_decisions'] or 0,
            'approved': row['approved'] or 0,
            'rejected': row['rejected'] or 0,
            'approval_rate': ((row['approved'] or 0) / (row['total_decisions'] or 1)) * 100,
            'avg_profit': row['avg_profit'] or 0,
            'total_profit': row['total_profit'] or 0
        }
    
    def get_negotiation_insights(self) -> Dict:
        """رؤى من عمليات التفاوض"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(success) as successful,
                AVG(final_deal - initial_offer) as avg_improvement,
                strategy_used,
                COUNT(*) as strategy_count
            FROM negotiations
            GROUP BY strategy_used
            ORDER BY successful DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return {
            'strategies': [dict(row) for row in rows],
            'best_strategy': rows[0]['strategy_used'] if rows else None
        }
    
    def get_recent_mistakes(self, limit: int = 10) -> List[Dict]:
        """الحصول على الأخطاء الأخيرة والدروس المستفادة"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM mistakes
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ==================== تحديث الأنماط ====================
    
    def _update_success_pattern(self, category: str, input_data: Dict):
        """تحديث أنماط النجاح"""
        # استخراج السمات الرئيسية
        key_features = self._extract_key_features(input_data)
        pattern_key = json.dumps(key_features, sort_keys=True)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # التحقق من وجود النمط
        cursor.execute("""
            SELECT id, occurrence_count, success_rate FROM success_patterns
            WHERE pattern_type = ? AND pattern_data = ?
        """, (category, pattern_key))
        
        existing = cursor.fetchone()
        
        if existing:
            # تحديث النمط الموجود
            new_count = existing['occurrence_count'] + 1
            cursor.execute("""
                UPDATE success_patterns
                SET occurrence_count = ?, last_seen = ?, 
                    success_rate = MIN(1.0, success_rate + 0.01)
                WHERE id = ?
            """, (new_count, datetime.now().isoformat(), existing['id']))
        else:
            # إضافة نمط جديد
            cursor.execute("""
                INSERT INTO success_patterns
                (pattern_type, pattern_data, success_rate, occurrence_count, 
                 last_seen, confidence)
                VALUES (?, ?, 0.5, 1, ?, 0.3)
            """, (category, pattern_key, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _extract_key_features(self, data: Dict) -> Dict:
        """استخراج السمات الرئيسية من البيانات"""
        features = {}
        
        # استخراج السمات المهمة فقط
        important_keys = ['site_type', 'score_range', 'price_range', 
                         'service_type', 'client_type', 'market']
        
        for key in important_keys:
            if key in data:
                features[key] = data[key]
        
        return features
    
    # ==================== التعلم والتوصيات ====================
    
    def get_recommendation(self, category: str, input_data: Dict) -> Dict:
        """الحصول على توصية بناءً على التجارب السابقة"""
        # الحصول على تجارب مشابهة
        similar = self.get_similar_experiences(category, input_data, limit=20)
        
        if not similar:
            return {
                'recommendation': 'no_data',
                'confidence': 0,
                'reason': 'لا توجد تجارب سابقة في هذه الفئة'
            }
        
        # حساب معدل النجاح
        successes = sum(1 for exp in similar if exp['success'])
        success_rate = successes / len(similar) * 100
        
        # الحصول على أفضل الاستراتيجيات
        best_strategies = self.get_best_strategies(category, limit=3)
        
        # الحصول على الدروس المستفادة
        lessons = [exp['lessons_learned'] for exp in similar 
                  if exp['lessons_learned'] and exp['success']]
        
        return {
            'recommendation': 'proceed' if success_rate > 60 else 'caution',
            'confidence': success_rate / 100,
            'success_rate': success_rate,
            'sample_size': len(similar),
            'best_strategies': best_strategies,
            'lessons': lessons[:5],
            'reason': f'بناءً على {len(similar)} تجربة سابقة، معدل النجاح {success_rate:.1f}%'
        }
    
    def get_learning_summary(self) -> Dict:
        """ملخص التعلم من التجارب"""
        categories = ['site_analysis', 'sales', 'purchase', 'negotiation', 'marketing']
        
        summary = {}
        for category in categories:
            stats = self.get_success_rate(category, days=30)
            summary[category] = stats
        
        # الإجمالي
        total_experiences = sum(s['total'] for s in summary.values())
        total_success = sum(s['successful'] for s in summary.values())
        total_revenue = sum(s['total_revenue'] for s in summary.values())
        total_loss = sum(s['total_loss'] for s in summary.values())
        
        return {
            'categories': summary,
            'total_experiences': total_experiences,
            'total_success': total_success,
            'overall_success_rate': (total_success / total_experiences * 100) if total_experiences > 0 else 0,
            'total_revenue': total_revenue,
            'total_loss': total_loss,
            'net_profit': total_revenue - total_loss
        }
