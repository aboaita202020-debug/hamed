"""
Smart Sales Database - قاعدة بيانات البائع الذكي المتكيف
يتعلم من كل عملية بيع ناجحة ويتكيف مع نوع الخدمة
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class SmartSalesDatabase:
    """قاعدة بيانات ذكية للبائع المتكيف"""
    
    def __init__(self, db_path: str = "smart_sales.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول أنواع الخدمات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                base_price REAL,
                description TEXT,
                success_rate REAL DEFAULT 0,
                total_sales INTEGER DEFAULT 0,
                avg_revenue REAL DEFAULT 0,
                best_strategies TEXT,
                created_at TEXT
            )
        """)
        
        # جدول استراتيجيات البيع حسب نوع الخدمة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_type TEXT NOT NULL,
                strategy_name TEXT NOT NULL,
                approach TEXT,
                message_template TEXT,
                pricing_strategy TEXT,
                success_rate REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                avg_revenue REAL DEFAULT 0,
                best_for_client_type TEXT,
                last_used TEXT,
                created_at TEXT
            )
        """)
        
        # جدول سلوك العملاء
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_behaviors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                service_type TEXT,
                behavior_pattern TEXT,
                objections TEXT,
                preferred_communication TEXT,
                price_sensitivity TEXT,
                decision_speed TEXT,
                success_rate REAL DEFAULT 0,
                total_interactions INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        
        # جدول عمليات البيع
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                service_type TEXT NOT NULL,
                strategy_used TEXT,
                approach TEXT,
                initial_price REAL,
                final_price REAL,
                objections_handled TEXT,
                outcome TEXT,
                revenue REAL,
                duration_days INTEGER,
                lessons_learned TEXT,
                client_feedback TEXT,
                created_at TEXT
            )
        """)
        
        # جدول تكيف الاستراتيجيات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strategy_adaptations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_type TEXT NOT NULL,
                client_type TEXT,
                adaptation TEXT,
                success_rate REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                notes TEXT,
                created_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ============ إدارة أنواع الخدمات ============
    
    def register_service_type(self, name: str, category: str = None, 
                             base_price: float = None, description: str = None) -> int:
        """تسجيل نوع خدمة جديد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO service_types (name, category, base_price, description, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, base_price, description, datetime.now().isoformat()))
            
            service_id = cursor.lastrowid
            conn.commit()
            return service_id
        except sqlite3.IntegrityError:
            # الخدمة موجودة بالفعل
            cursor.execute("SELECT id FROM service_types WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def get_service_type(self, name: str) -> Optional[Dict]:
        """الحصول على معلومات نوع الخدمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM service_types WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def update_service_stats(self, service_name: str, success: bool, revenue: float = 0):
        """تحديث إحصائيات نوع الخدمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_sales, success_rate, avg_revenue 
            FROM service_types WHERE name = ?
        """, (service_name,))
        
        result = cursor.fetchone()
        if result:
            total_sales, current_rate, avg_rev = result
            new_total = total_sales + 1
            
            if success:
                new_rate = ((current_rate * total_sales) + 100) / new_total
                new_avg = ((avg_rev * total_sales) + revenue) / new_total
            else:
                new_rate = (current_rate * total_sales) / new_total
                new_avg = avg_rev
            
            cursor.execute("""
                UPDATE service_types 
                SET total_sales = ?, success_rate = ?, avg_revenue = ?
                WHERE name = ?
            """, (new_total, new_rate, new_avg, service_name))
            
            conn.commit()
        
        conn.close()
    
    # ============ إدارة استراتيجيات البيع ============
    
    def add_strategy(self, service_type: str, strategy_name: str, 
                    approach: str = None, message_template: str = None,
                    pricing_strategy: str = None, best_for_client_type: str = None) -> int:
        """إضافة استراتيجية بيع جديدة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sales_strategies 
            (service_type, strategy_name, approach, message_template, 
             pricing_strategy, best_for_client_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (service_type, strategy_name, approach, message_template,
              pricing_strategy, best_for_client_type, datetime.now().isoformat()))
        
        strategy_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return strategy_id
    
    def get_best_strategies(self, service_type: str, limit: int = 5) -> List[Dict]:
        """الحصول على أفضل الاستراتيجيات لنوع خدمة معين"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM sales_strategies 
            WHERE service_type = ?
            ORDER BY success_rate DESC, usage_count DESC
            LIMIT ?
        """, (service_type, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    def update_strategy_stats(self, strategy_id: int, success: bool, revenue: float = 0):
        """تحديث إحصائيات الاستراتيجية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT usage_count, success_count, success_rate, avg_revenue
            FROM sales_strategies WHERE id = ?
        """, (strategy_id,))
        
        result = cursor.fetchone()
        if result:
            usage_count, success_count, current_rate, avg_rev = result
            new_usage = usage_count + 1
            
            if success:
                new_success = success_count + 1
                new_rate = ((current_rate * usage_count) + 100) / new_usage
                new_avg = ((avg_rev * usage_count) + revenue) / new_usage
            else:
                new_success = success_count
                new_rate = (current_rate * usage_count) / new_usage
                new_avg = avg_rev
            
            cursor.execute("""
                UPDATE sales_strategies 
                SET usage_count = ?, success_count = ?, success_rate = ?, 
                    avg_revenue = ?, last_used = ?
                WHERE id = ?
            """, (new_usage, new_success, new_rate, new_avg, 
                  datetime.now().isoformat(), strategy_id))
            
            conn.commit()
        
        conn.close()
    
    # ============ تحليل سلوك العملاء ============
    
    def record_client_behavior(self, client_id: str, service_type: str,
                              behavior_pattern: str = None, objections: str = None,
                              preferred_communication: str = None,
                              price_sensitivity: str = None,
                              decision_speed: str = None, success: bool = None):
        """تسجيل سلوك العميل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود سجل سابق
        cursor.execute("""
            SELECT id, total_interactions, success_rate 
            FROM client_behaviors 
            WHERE client_id = ? AND service_type = ?
        """, (client_id, service_type))
        
        result = cursor.fetchone()
        
        if result:
            # تحديث السجل الموجود
            behavior_id, total_interactions, current_rate = result
            new_total = total_interactions + 1
            
            if success is not None:
                if success:
                    new_rate = ((current_rate * total_interactions) + 100) / new_total
                else:
                    new_rate = (current_rate * total_interactions) / new_total
                
                cursor.execute("""
                    UPDATE client_behaviors 
                    SET behavior_pattern = COALESCE(?, behavior_pattern),
                        objections = COALESCE(?, objections),
                        preferred_communication = COALESCE(?, preferred_communication),
                        price_sensitivity = COALESCE(?, price_sensitivity),
                        decision_speed = COALESCE(?, decision_speed),
                        success_rate = ?,
                        total_interactions = ?
                    WHERE id = ?
                """, (behavior_pattern, objections, preferred_communication,
                      price_sensitivity, decision_speed, new_rate, new_total, behavior_id))
        else:
            # إنشاء سجل جديد
            success_rate = 100 if success else 0 if success is not None else 0
            
            cursor.execute("""
                INSERT INTO client_behaviors 
                (client_id, service_type, behavior_pattern, objections,
                 preferred_communication, price_sensitivity, decision_speed,
                 success_rate, total_interactions, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (client_id, service_type, behavior_pattern, objections,
                  preferred_communication, price_sensitivity, decision_speed,
                  success_rate, 1, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_client_profile(self, client_id: str, service_type: str = None) -> Optional[Dict]:
        """الحصول على ملف العميل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if service_type:
            cursor.execute("""
                SELECT * FROM client_behaviors 
                WHERE client_id = ? AND service_type = ?
            """, (client_id, service_type))
        else:
            cursor.execute("""
                SELECT * FROM client_behaviors 
                WHERE client_id = ?
                ORDER BY total_interactions DESC
                LIMIT 1
            """, (client_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    # ============ تسجيل عمليات البيع ============
    
    def record_sale(self, client_id: str, service_type: str, strategy_used: str,
                   approach: str = None, initial_price: float = None,
                   final_price: float = None, objections_handled: str = None,
                   outcome: str = None, revenue: float = None,
                   duration_days: int = None, lessons_learned: str = None,
                   client_feedback: str = None) -> int:
        """تسجيل عملية بيع"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sales 
            (client_id, service_type, strategy_used, approach, initial_price,
             final_price, objections_handled, outcome, revenue, duration_days,
             lessons_learned, client_feedback, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (client_id, service_type, strategy_used, approach, initial_price,
              final_price, objections_handled, outcome, revenue, duration_days,
              lessons_learned, client_feedback, datetime.now().isoformat()))
        
        sale_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # تحديث إحصائيات نوع الخدمة
        success = outcome == 'success'
        self.update_service_stats(service_type, success, revenue or 0)
        
        return sale_id
    
    # ============ التكيف التلقائي ============
    
    def adapt_strategy(self, service_type: str, client_type: str,
                      adaptation: str, success: bool = None, notes: str = None):
        """تسجيل تكيف الاستراتيجية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود تكيف سابق
        cursor.execute("""
            SELECT id, usage_count, success_rate 
            FROM strategy_adaptations 
            WHERE service_type = ? AND client_type = ?
        """, (service_type, client_type))
        
        result = cursor.fetchone()
        
        if result:
            adaptation_id, usage_count, current_rate = result
            new_usage = usage_count + 1
            
            if success is not None:
                if success:
                    new_rate = ((current_rate * usage_count) + 100) / new_usage
                else:
                    new_rate = (current_rate * usage_count) / new_usage
                
                cursor.execute("""
                    UPDATE strategy_adaptations 
                    SET adaptation = ?, success_rate = ?, usage_count = ?, notes = ?
                    WHERE id = ?
                """, (adaptation, new_rate, new_usage, notes, adaptation_id))
        else:
            success_rate = 100 if success else 0 if success is not None else 0
            
            cursor.execute("""
                INSERT INTO strategy_adaptations 
                (service_type, client_type, adaptation, success_rate, usage_count, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (service_type, client_type, adaptation, success_rate, 1,
                  notes, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_adaptation(self, service_type: str, client_type: str) -> Optional[Dict]:
        """الحصول على التكيف المناسب"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM strategy_adaptations 
            WHERE service_type = ? AND client_type = ?
            ORDER BY success_rate DESC, usage_count DESC
            LIMIT 1
        """, (service_type, client_type))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    # ============ التحليلات والتقارير ============
    
    def get_sales_analytics(self, service_type: str = None, days: int = 30) -> Dict:
        """تحليلات المبيعات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                COUNT(*) as total_sales,
                SUM(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) as successful_sales,
                SUM(revenue) as total_revenue,
                AVG(revenue) as avg_revenue,
                AVG(duration_days) as avg_duration
            FROM sales
            WHERE created_at >= datetime('now', ?)
        """
        
        params = [f'-{days} days']
        
        if service_type:
            query += " AND service_type = ?"
            params.append(service_type)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        analytics = {
            'total_sales': result[0] or 0,
            'successful_sales': result[1] or 0,
            'total_revenue': result[2] or 0,
            'avg_revenue': result[3] or 0,
            'avg_duration': result[4] or 0,
            'success_rate': (result[1] / result[0] * 100) if result[0] > 0 else 0
        }
        
        conn.close()
        return analytics
    
    def get_top_performing_strategies(self, service_type: str = None, limit: int = 10) -> List[Dict]:
        """الحصول على أفضل الاستراتيجيات أداءً"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM sales_strategies
            WHERE usage_count > 0
        """
        
        params = []
        if service_type:
            query += " AND service_type = ?"
            params.append(service_type)
        
        query += " ORDER BY success_rate DESC, avg_revenue DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        strategies = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return strategies
