"""
Call System Database - قاعدة بيانات نظام المكالمات
تدير كل المكالمات مع العملاء وتسجل التفاصيل
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

class CallDatabase:
    """قاعدة بيانات نظام المكالمات"""
    
    def __init__(self, db_path: str = "call_system.db"):
        self.db_path = db_path
        self.phone_number = "01061245527"
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول المكالمات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_id TEXT UNIQUE NOT NULL,
                client_id TEXT,
                client_name TEXT,
                client_phone TEXT,
                direction TEXT NOT NULL,
                status TEXT NOT NULL,
                duration_seconds INTEGER DEFAULT 0,
                call_type TEXT,
                purpose TEXT,
                outcome TEXT,
                notes TEXT,
                recording_url TEXT,
                started_at TEXT,
                ended_at TEXT,
                created_at TEXT
            )
        """)
        
        # جدول جهات الاتصال
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                company TEXT,
                service_type TEXT,
                status TEXT DEFAULT 'active',
                total_calls INTEGER DEFAULT 0,
                total_duration INTEGER DEFAULT 0,
                last_call TEXT,
                notes TEXT,
                created_at TEXT
            )
        """)
        
        # جدول سجل المكالمات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (call_id) REFERENCES calls(call_id)
            )
        """)
        
        # جدول قوالب المكالمات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                service_type TEXT,
                script TEXT NOT NULL,
                opening TEXT,
                closing TEXT,
                key_points TEXT,
                success_rate REAL DEFAULT 0,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        
        # جدول إحصائيات المكالمات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_calls INTEGER DEFAULT 0,
                incoming_calls INTEGER DEFAULT 0,
                outgoing_calls INTEGER DEFAULT 0,
                completed_calls INTEGER DEFAULT 0,
                missed_calls INTEGER DEFAULT 0,
                total_duration INTEGER DEFAULT 0,
                avg_duration REAL DEFAULT 0,
                success_rate REAL DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ============ إدارة المكالمات ============
    
    def create_call(self, client_id: str = None, client_name: str = None,
                   client_phone: str = None, direction: str = 'outgoing',
                   call_type: str = 'sales', purpose: str = None) -> str:
        """إنشاء مكالمة جديدة"""
        call_id = f"CALL-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO calls 
            (call_id, client_id, client_name, client_phone, direction, 
             status, call_type, purpose, started_at, created_at)
            VALUES (?, ?, ?, ?, ?, 'ringing', ?, ?, ?, ?)
        """, (call_id, client_id, client_name, client_phone, direction,
              call_type, purpose, datetime.now().isoformat(), datetime.now().isoformat()))
        
        # تسجيل حدث البداية
        self._log_call_event(call_id, 'call_started', {
            'direction': direction,
            'call_type': call_type
        })
        
        conn.commit()
        conn.close()
        
        return call_id
    
    def update_call_status(self, call_id: str, status: str, 
                          duration: int = None, outcome: str = None,
                          notes: str = None):
        """تحديث حالة المكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = ["status = ?"]
        params = [status]
        
        if duration is not None:
            updates.append("duration_seconds = ?")
            params.append(duration)
        
        if outcome:
            updates.append("outcome = ?")
            params.append(outcome)
        
        if notes:
            updates.append("notes = ?")
            params.append(notes)
        
        if status == 'completed':
            updates.append("ended_at = ?")
            params.append(datetime.now().isoformat())
        
        params.append(call_id)
        
        cursor.execute(f"""
            UPDATE calls 
            SET {', '.join(updates)}
            WHERE call_id = ?
        """, params)
        
        # تسجيل حدث التحديث
        self._log_call_event(call_id, 'status_updated', {
            'status': status,
            'duration': duration,
            'outcome': outcome
        })
        
        conn.commit()
        conn.close()
    
    def get_call(self, call_id: str) -> Optional[Dict]:
        """الحصول على تفاصيل مكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM calls WHERE call_id = ?", (call_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            call = dict(zip(columns, row))
            
            # جلب سجل الأحداث
            cursor.execute("""
                SELECT * FROM call_logs 
                WHERE call_id = ? 
                ORDER BY timestamp
            """, (call_id,))
            
            logs = cursor.fetchall()
            log_columns = [desc[0] for desc in cursor.description]
            call['logs'] = [dict(zip(log_columns, log)) for log in logs]
            
            conn.close()
            return call
        
        conn.close()
        return None
    
    def get_active_calls(self) -> List[Dict]:
        """الحصول على المكالمات النشطة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM calls 
            WHERE status IN ('ringing', 'in_progress')
            ORDER BY started_at DESC
        """)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        calls = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return calls
    
    def get_call_history(self, client_id: str = None, limit: int = 50) -> List[Dict]:
        """الحصول على سجل المكالمات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if client_id:
            cursor.execute("""
                SELECT * FROM calls 
                WHERE client_id = ?
                ORDER BY started_at DESC
                LIMIT ?
            """, (client_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM calls 
                ORDER BY started_at DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        calls = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return calls
    
    def _log_call_event(self, call_id: str, event_type: str, event_data: Dict):
        """تسجيل حدث مكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO call_logs (call_id, event_type, event_data, timestamp)
            VALUES (?, ?, ?, ?)
        """, (call_id, event_type, json.dumps(event_data), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    # ============ إدارة جهات الاتصال ============
    
    def add_contact(self, name: str, phone: str, email: str = None,
                   company: str = None, service_type: str = None) -> str:
        """إضافة جهة اتصال جديدة"""
        contact_id = f"CONT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO contacts 
            (contact_id, name, phone, email, company, service_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (contact_id, name, phone, email, company, service_type, 
              datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return contact_id
    
    def update_contact_after_call(self, contact_id: str, duration: int):
        """تحديث جهة اتصال بعد مكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE contacts 
            SET total_calls = total_calls + 1,
                total_duration = total_duration + ?,
                last_call = ?
            WHERE contact_id = ?
        """, (duration, datetime.now().isoformat(), contact_id))
        
        conn.commit()
        conn.close()
    
    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """الحصول على جهة اتصال"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM contacts WHERE contact_id = ?", (contact_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return dict(zip(columns, row))
        
        conn.close()
        return None
    
    def get_all_contacts(self, status: str = None) -> List[Dict]:
        """الحصول على كل جهات الاتصال"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM contacts WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM contacts")
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        contacts = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return contacts
    
    # ============ قوالب المكالمات ============
    
    def add_call_template(self, name: str, script: str, 
                         service_type: str = None, opening: str = None,
                         closing: str = None, key_points: str = None) -> int:
        """إضافة قالب مكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO call_templates 
            (name, script, service_type, opening, closing, key_points, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, script, service_type, opening, closing, key_points,
              datetime.now().isoformat()))
        
        template_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return template_id
    
    def get_call_template(self, service_type: str = None) -> Optional[Dict]:
        """الحصول على قالب مكالمة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if service_type:
            cursor.execute("""
                SELECT * FROM call_templates 
                WHERE service_type = ?
                ORDER BY success_rate DESC, usage_count DESC
                LIMIT 1
            """, (service_type,))
        else:
            cursor.execute("""
                SELECT * FROM call_templates 
                ORDER BY success_rate DESC, usage_count DESC
                LIMIT 1
            """)
        
        row = cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return dict(zip(columns, row))
        
        conn.close()
        return None
    
    def update_template_stats(self, template_id: int, success: bool):
        """تحديث إحصائيات القالب"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT usage_count, success_rate FROM call_templates WHERE id = ?
        """, (template_id,))
        
        result = cursor.fetchone()
        if result:
            usage_count, current_rate = result
            new_usage = usage_count + 1
            
            if success:
                new_rate = ((current_rate * usage_count) + 100) / new_usage
            else:
                new_rate = (current_rate * usage_count) / new_usage
            
            cursor.execute("""
                UPDATE call_templates 
                SET usage_count = ?, success_rate = ?
                WHERE id = ?
            """, (new_usage, new_rate, template_id))
            
            conn.commit()
        
        conn.close()
    
    # ============ الإحصائيات ============
    
    def update_daily_stats(self, date: str = None):
        """تحديث الإحصائيات اليومية"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # حساب الإحصائيات
        cursor.execute("""
            SELECT 
                COUNT(*) as total_calls,
                SUM(CASE WHEN direction = 'incoming' THEN 1 ELSE 0 END) as incoming,
                SUM(CASE WHEN direction = 'outgoing' THEN 1 ELSE 0 END) as outgoing,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'missed' THEN 1 ELSE 0 END) as missed,
                SUM(duration_seconds) as total_duration,
                AVG(duration_seconds) as avg_duration
            FROM calls
            WHERE DATE(started_at) = ?
        """, (date,))
        
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            total_calls, incoming, outgoing, completed, missed, total_duration, avg_duration = result
            
            success_rate = (completed / total_calls * 100) if total_calls > 0 else 0
            
            # حفظ أو تحديث الإحصائيات
            cursor.execute("""
                INSERT OR REPLACE INTO call_stats 
                (date, total_calls, incoming_calls, outgoing_calls, 
                 completed_calls, missed_calls, total_duration, avg_duration, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, total_calls, incoming, outgoing, completed, missed,
                  total_duration or 0, avg_duration or 0, success_rate))
            
            conn.commit()
        
        conn.close()
    
    def get_call_stats(self, days: int = 7) -> List[Dict]:
        """الحصول على إحصائيات المكالمات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM call_stats 
            WHERE date >= date('now', ?)
            ORDER BY date DESC
        """, (f'-{days} days',))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        stats = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return stats
    
    def get_overall_stats(self) -> Dict:
        """الحصول على الإحصائيات العامة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_calls,
                SUM(CASE WHEN direction = 'incoming' THEN 1 ELSE 0 END) as incoming,
                SUM(CASE WHEN direction = 'outgoing' THEN 1 ELSE 0 END) as outgoing,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'missed' THEN 1 ELSE 0 END) as missed,
                SUM(duration_seconds) as total_duration,
                AVG(duration_seconds) as avg_duration
            FROM calls
        """)
        
        result = cursor.fetchone()
        
        if result:
            total_calls, incoming, outgoing, completed, missed, total_duration, avg_duration = result
            
            # عدد جهات الاتصال
            cursor.execute("SELECT COUNT(*) FROM contacts")
            total_contacts = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_calls': total_calls or 0,
                'incoming_calls': incoming or 0,
                'outgoing_calls': outgoing or 0,
                'completed_calls': completed or 0,
                'missed_calls': missed or 0,
                'total_duration': total_duration or 0,
                'avg_duration': avg_duration or 0,
                'total_contacts': total_contacts,
                'success_rate': (completed / total_calls * 100) if total_calls > 0 else 0
            }
        
        conn.close()
        return {
            'total_calls': 0, 'incoming_calls': 0, 'outgoing_calls': 0,
            'completed_calls': 0, 'missed_calls': 0, 'total_duration': 0,
            'avg_duration': 0, 'total_contacts': 0, 'success_rate': 0
        }
