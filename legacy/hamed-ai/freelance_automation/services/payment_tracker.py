"""
Payment Tracker - Tracks all revenue and payments
"""
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from core.database import Database
from core.logger import logger

class PaymentTracker:
    """Tracks revenue, payments, and financial metrics"""
    
    def __init__(self):
        self.db = Database()
        self._init_payment_tables()
        logger.info("PaymentTracker initialized")
    
    def _init_payment_tables(self):
        """Initialize payment tracking tables"""
        try:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    platform TEXT NOT NULL,
                    payment_method TEXT,
                    status TEXT DEFAULT 'pending',
                    received_at TEXT,
                    created_at TEXT NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    description TEXT,
                    recorded_at TEXT NOT NULL
                )
            """)
            
            logger.debug("Payment tables initialized")
        except Exception as e:
            logger.error(f"Failed to initialize payment tables: {e}")
    
    def record_payment(self, order_id: str, amount: float, platform: str,
                      payment_method: str = "platform", status: str = "completed") -> str:
        """Record a payment received"""
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            self.db.execute("""
                INSERT INTO payments (id, order_id, amount, platform, payment_method, status, received_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (payment_id, order_id, amount, platform, payment_method, status,
                  datetime.now().isoformat(), datetime.now().isoformat()))
            
            logger.info(f"Payment recorded: {payment_id} - ${amount} from {platform}")
            return payment_id
        
        except Exception as e:
            logger.error(f"Failed to record payment: {e}")
            raise
    
    def record_expense(self, category: str, amount: float, description: str = "") -> str:
        """Record an expense"""
        expense_id = f"EXP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        try:
            self.db.execute("""
                INSERT INTO expenses (id, category, amount, description, recorded_at)
                VALUES (?, ?, ?, ?, ?)
            """, (expense_id, category, amount, description, datetime.now().isoformat()))
            
            logger.info(f"Expense recorded: {expense_id} - ${amount} ({category})")
            return expense_id
        
        except Exception as e:
            logger.error(f"Failed to record expense: {e}")
            raise
    
    def get_revenue_summary(self, days: int = 30) -> Dict:
        """Get revenue summary for period"""
        try:
            result = self.db.fetch_one("""
                SELECT 
                    COUNT(*) as total_payments,
                    COALESCE(SUM(amount), 0) as total_revenue,
                    COALESCE(AVG(amount), 0) as avg_payment
                FROM payments
                WHERE status = 'completed'
                AND received_at >= datetime('now', ?)
            """, (f"-{days} days",))
            
            return {
                "period_days": days,
                "total_payments": result['total_payments'] if result else 0,
                "total_revenue": result['total_revenue'] if result else 0,
                "avg_payment": result['avg_payment'] if result else 0,
            }
        
        except Exception as e:
            logger.error(f"Revenue summary failed: {e}")
            return {"period_days": days, "total_payments": 0, "total_revenue": 0, "avg_payment": 0}
    
    def get_expense_summary(self, days: int = 30) -> Dict:
        """Get expense summary for period"""
        try:
            result = self.db.fetch_one("""
                SELECT 
                    COUNT(*) as total_expenses,
                    COALESCE(SUM(amount), 0) as total_expenses_amount
                FROM expenses
                WHERE recorded_at >= datetime('now', ?)
            """, (f"-{days} days",))
            
            return {
                "period_days": days,
                "total_expenses": result['total_expenses'] if result else 0,
                "total_amount": result['total_expenses_amount'] if result else 0,
            }
        
        except Exception as e:
            logger.error(f"Expense summary failed: {e}")
            return {"period_days": days, "total_expenses": 0, "total_amount": 0}
    
    def get_profit_summary(self, days: int = 30) -> Dict:
        """Get profit summary (revenue - expenses)"""
        revenue = self.get_revenue_summary(days)
        expenses = self.get_expense_summary(days)
        
        total_revenue = revenue['total_revenue']
        total_expenses = expenses['total_amount']
        profit = total_revenue - total_expenses
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "period_days": days,
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "profit": profit,
            "profit_margin": round(profit_margin, 2),
        }
    
    def get_revenue_by_platform(self, days: int = 30) -> Dict[str, float]:
        """Get revenue breakdown by platform"""
        try:
            results = self.db.fetch_all("""
                SELECT platform, SUM(amount) as total
                FROM payments
                WHERE status = 'completed'
                AND received_at >= datetime('now', ?)
                GROUP BY platform
                ORDER BY total DESC
            """, (f"-{days} days",))
            
            return {row['platform']: row['total'] for row in results}
        
        except Exception as e:
            logger.error(f"Revenue by platform failed: {e}")
            return {}
    
    def get_revenue_by_service(self, days: int = 30) -> Dict[str, float]:
        """Get revenue breakdown by service type"""
        try:
            results = self.db.fetch_all("""
                SELECT o.service_type, SUM(p.amount) as total
                FROM payments p
                JOIN orders o ON p.order_id = o.id
                WHERE p.status = 'completed'
                AND p.received_at >= datetime('now', ?)
                GROUP BY o.service_type
                ORDER BY total DESC
            """, (f"-{days} days",))
            
            return {row['service_type']: row['total'] for row in results}
        
        except Exception as e:
            logger.error(f"Revenue by service failed: {e}")
            return {}
    
    def get_daily_revenue(self, days: int = 30) -> List[Dict]:
        """Get daily revenue for chart"""
        try:
            results = self.db.fetch_all("""
                SELECT 
                    DATE(received_at) as date,
                    SUM(amount) as total,
                    COUNT(*) as count
                FROM payments
                WHERE status = 'completed'
                AND received_at >= datetime('now', ?)
                GROUP BY DATE(received_at)
                ORDER BY date
            """, (f"-{days} days",))
            
            return results
        
        except Exception as e:
            logger.error(f"Daily revenue failed: {e}")
            return []
    
    def get_financial_dashboard(self) -> Dict:
        """Get complete financial dashboard"""
        return {
            "revenue_30d": self.get_revenue_summary(30),
            "revenue_7d": self.get_revenue_summary(7),
            "expenses_30d": self.get_expense_summary(30),
            "profit_30d": self.get_profit_summary(30),
            "by_platform": self.get_revenue_by_platform(30),
            "by_service": self.get_revenue_by_service(30),
            "daily_trend": self.get_daily_revenue(30),
            "timestamp": datetime.now().isoformat(),
        }
