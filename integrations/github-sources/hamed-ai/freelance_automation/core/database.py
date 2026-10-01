"""
Database Layer - SQLite with async-safe operations
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
import threading

from .config import Config

class Database:
    """Thread-safe SQLite database manager"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize database connection"""
        if self._initialized:
            return
        
        self.db_path = Config.DB_PATH
        self._local = threading.local()
        self._init_schema()
        self._initialized = True
    
    def _get_connection(self):
        """Get thread-local connection"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path))
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    def _init_schema(self):
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                service_type TEXT NOT NULL,
                client_name TEXT NOT NULL,
                client_email TEXT,
                description TEXT NOT NULL,
                requirements TEXT,
                status TEXT DEFAULT 'pending',
                assigned_brain TEXT,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                delivered_at TEXT,
                result TEXT,
                quality_score REAL,
                notes TEXT
            )
        """)
        
        # Brains table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS brains (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                specialty TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                total_tasks INTEGER DEFAULT 0,
                successful_tasks INTEGER DEFAULT 0,
                failed_tasks INTEGER DEFAULT 0,
                last_used TEXT,
                avg_response_time REAL DEFAULT 0
            )
        """)
        
        # Services table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                base_price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                brain_id TEXT NOT NULL,
                enabled INTEGER DEFAULT 1,
                total_orders INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0,
                avg_rating REAL DEFAULT 0,
                FOREIGN KEY (brain_id) REFERENCES brains(id)
            )
        """)
        
        # Revenue tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                platform TEXT NOT NULL,
                service_type TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)
        
        # Audit log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                details TEXT,
                user TEXT DEFAULT 'system'
            )
        """)
        
        # Website analyses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS website_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                domain TEXT NOT NULL,
                site_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                analysis TEXT,
                recommendations TEXT,
                services TEXT,
                analyzed_at TEXT NOT NULL
            )
        """)
        
        # Messages
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                message TEXT NOT NULL,
                contact_info TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                sent_at TEXT
            )
        """)
        
        # Initialize brains from config
        for brain_id, brain_config in Config.AI_BRAINS.items():
            cursor.execute("""
                INSERT OR IGNORE INTO brains (id, name, provider, model, specialty)
                VALUES (?, ?, ?, ?, ?)
            """, (brain_id, brain_config['name'], brain_config['provider'], 
                  brain_config['model'], brain_config['specialty']))
        
        # Initialize services from config
        for service_name, service_config in Config.SERVICES.items():
            cursor.execute("""
                INSERT OR IGNORE INTO services (id, name, description, base_price, brain_id, enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (service_name, service_name.replace('_', ' ').title(),
                  f"{service_name.replace('_', ' ').title()} service",
                  service_config['base_price'], service_config['brain'],
                  1 if service_config['enabled'] else 0))
        
        conn.commit()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute query with error handling"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {e}")
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    # Order operations
    def create_order(self, order_data: Dict) -> str:
        """Create new order"""
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        self.execute("""
            INSERT INTO orders (id, platform, service_type, client_name, client_email,
                              description, requirements, price, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_id, order_data['platform'], order_data['service_type'],
              order_data['client_name'], order_data.get('client_email', ''),
              order_data['description'], json.dumps(order_data.get('requirements', {})),
              order_data['price'], datetime.now().isoformat()))
        
        self.log_audit('CREATE', 'order', order_id, order_data)
        return order_id
    
    def update_order_status(self, order_id: str, status: str, **kwargs):
        """Update order status"""
        updates = ["status = ?"]
        params = [status]
        
        if 'assigned_brain' in kwargs:
            updates.append("assigned_brain = ?")
            params.append(kwargs['assigned_brain'])
        
        if 'result' in kwargs:
            updates.append("result = ?")
            params.append(json.dumps(kwargs['result']))
        
        if 'quality_score' in kwargs:
            updates.append("quality_score = ?")
            params.append(kwargs['quality_score'])
        
        if status == 'in_progress':
            updates.append("started_at = ?")
            params.append(datetime.now().isoformat())
        elif status == 'completed':
            updates.append("completed_at = ?")
            params.append(datetime.now().isoformat())
        elif status == 'delivered':
            updates.append("delivered_at = ?")
            params.append(datetime.now().isoformat())
        
        params.append(order_id)
        self.execute(f"UPDATE orders SET {', '.join(updates)} WHERE id = ?", tuple(params))
        self.log_audit('UPDATE', 'order', order_id, {'status': status, **kwargs})
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID"""
        return self.fetch_one("SELECT * FROM orders WHERE id = ?", (order_id,))
    
    def get_pending_orders(self) -> List[Dict]:
        """Get all pending orders"""
        return self.fetch_all("SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at")
    
    # Brain operations
    def update_brain_stats(self, brain_id: str, success: bool, response_time: float):
        """Update brain statistics"""
        if success:
            self.execute("""
                UPDATE brains 
                SET total_tasks = total_tasks + 1,
                    successful_tasks = successful_tasks + 1,
                    last_used = ?,
                    avg_response_time = (avg_response_time * (total_tasks - 1) + ?) / total_tasks
                WHERE id = ?
            """, (datetime.now().isoformat(), response_time, brain_id))
        else:
            self.execute("""
                UPDATE brains 
                SET total_tasks = total_tasks + 1,
                    failed_tasks = failed_tasks + 1,
                    last_used = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), brain_id))
    
    def get_available_brain(self, specialty: str) -> Optional[Dict]:
        """Get available brain for specialty"""
        return self.fetch_one("""
            SELECT * FROM brains 
            WHERE specialty = ? AND status = 'active'
            ORDER BY successful_tasks DESC
            LIMIT 1
        """, (specialty,))
    
    # Revenue operations
    def record_revenue(self, order_id: str, amount: float, platform: str, service_type: str):
        """Record revenue from completed order"""
        self.execute("""
            INSERT INTO revenue (order_id, amount, platform, service_type, recorded_at)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, amount, platform, service_type, datetime.now().isoformat()))
        
        # Update service stats
        self.execute("""
            UPDATE services 
            SET total_orders = total_orders + 1,
                total_revenue = total_revenue + ?
            WHERE id = ?
        """, (amount, service_type))
    
    def get_revenue_summary(self, days: int = 30) -> Dict:
        """Get revenue summary for last N days"""
        result = self.fetch_one("""
            SELECT 
                COUNT(*) as total_orders,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_order_value
            FROM revenue
            WHERE recorded_at >= datetime('now', ?)
        """, (f"-{days} days",))
        
        return result or {'total_orders': 0, 'total_revenue': 0, 'avg_order_value': 0}
    
    # Audit operations
    def log_audit(self, action: str, entity_type: str, entity_id: str, details: Dict):
        """Log audit entry"""
        self.execute("""
            INSERT INTO audit_log (timestamp, action, entity_type, entity_id, details)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), action, entity_type, entity_id, json.dumps(details)))
