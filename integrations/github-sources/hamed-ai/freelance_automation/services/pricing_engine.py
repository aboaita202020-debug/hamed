"""
Dynamic Pricing Engine - AI-powered pricing optimization
"""
import time
from typing import Dict, List, Optional
from datetime import datetime

from core.database import Database
from core.logger import logger

class PricingEngine:
    """Dynamic pricing based on demand, competition, and quality"""
    
    def __init__(self):
        self.db = Database()
        self.base_prices = {
            "content_writing": {"basic": 15, "standard": 30, "premium": 60},
            "translation": {"basic": 10, "standard": 20, "premium": 40},
            "data_analysis": {"basic": 25, "standard": 50, "premium": 100},
            "code_generation": {"basic": 20, "standard": 45, "premium": 90},
        }
        
        logger.info("PricingEngine initialized")
    
    def calculate_price(self, service_type: str, tier: str = "standard", 
                       complexity: float = 1.0, urgency: float = 1.0,
                       demand_factor: float = 1.0) -> float:
        """
        Calculate dynamic price for a service
        
        Args:
            service_type: Type of service
            tier: Pricing tier (basic/standard/premium)
            complexity: Complexity multiplier (0.5-2.0)
            urgency: Urgency multiplier (1.0-3.0)
            demand_factor: Market demand multiplier (0.8-1.5)
        
        Returns:
            Calculated price in USD
        """
        start_time = time.time()
        
        try:
            # Get base price
            if service_type not in self.base_prices:
                raise ValueError(f"Unknown service type: {service_type}")
            
            base_price = self.base_prices[service_type].get(tier, 30)
            
            # Apply multipliers
            final_price = base_price * complexity * urgency * demand_factor
            
            # Round to nearest dollar
            final_price = round(final_price, 2)
            
            duration = time.time() - start_time
            logger.info(f"Price calculated: ${final_price} for {service_type} ({tier}) in {duration:.3f}s")
            
            return final_price
        
        except Exception as e:
            logger.error(f"Price calculation failed: {e}")
            # Return default price
            return 30.0
    
    def get_demand_factor(self, service_type: str) -> float:
        """
        Calculate demand factor based on recent orders
        
        Returns:
            Demand multiplier (0.8-1.5)
        """
        try:
            # Get orders from last 7 days
            recent_orders = self.db.fetch_all("""
                SELECT COUNT(*) as count 
                FROM orders 
                WHERE service_type = ? 
                AND created_at >= datetime('now', '-7 days')
            """, (service_type,))
            
            order_count = recent_orders[0]['count'] if recent_orders else 0
            
            # Calculate demand factor
            # More orders = higher demand = higher price
            if order_count > 20:
                return 1.5  # High demand
            elif order_count > 10:
                return 1.3  # Medium-high demand
            elif order_count > 5:
                return 1.1  # Medium demand
            else:
                return 1.0  # Normal demand
        
        except Exception as e:
            logger.error(f"Demand factor calculation failed: {e}")
            return 1.0
    
    def estimate_complexity(self, description: str) -> float:
        """
        Estimate task complexity from description
        
        Returns:
            Complexity multiplier (0.5-2.0)
        """
        # Simple keyword-based estimation
        # In production, use AI brain for better estimation
        
        high_complexity_keywords = ['research', 'analysis', 'comprehensive', 'detailed', 'complex']
        medium_complexity_keywords = ['write', 'create', 'develop', 'build', 'design']
        
        description_lower = description.lower()
        
        high_count = sum(1 for kw in high_complexity_keywords if kw in description_lower)
        medium_count = sum(1 for kw in medium_complexity_keywords if kw in description_lower)
        
        if high_count >= 2:
            return 1.8
        elif high_count == 1 or medium_count >= 2:
            return 1.4
        elif medium_count == 1:
            return 1.0
        else:
            return 0.8
    
    def calculate_urgency(self, deadline_hours: Optional[float] = None) -> float:
        """
        Calculate urgency multiplier based on deadline
        
        Returns:
            Urgency multiplier (1.0-3.0)
        """
        if deadline_hours is None:
            return 1.0
        
        if deadline_hours < 24:
            return 3.0  # Rush (24h)
        elif deadline_hours < 48:
            return 2.5  # Very urgent (48h)
        elif deadline_hours < 72:
            return 2.0  # Urgent (72h)
        elif deadline_hours < 168:  # 7 days
            return 1.5  # Somewhat urgent
        else:
            return 1.0  # Normal
    
    def optimize_pricing(self, service_type: str) -> Dict:
        """
        Optimize pricing for a service based on historical data
        
        Returns:
            Optimized pricing recommendations
        """
        try:
            # Get historical data
            orders = self.db.fetch_all("""
                SELECT price, status, created_at
                FROM orders
                WHERE service_type = ?
                AND created_at >= datetime('now', '-30 days')
            """, (service_type,))
            
            if not orders:
                return {"recommendation": "insufficient_data", "current_price": 30}
            
            # Calculate metrics
            total_orders = len(orders)
            completed_orders = len([o for o in orders if o['status'] == 'completed'])
            avg_price = sum(o['price'] for o in orders) / total_orders
            
            # Calculate conversion rate
            conversion_rate = completed_orders / total_orders if total_orders > 0 else 0
            
            # Pricing recommendations
            if conversion_rate < 0.3:
                recommendation = "lower_price"
                suggested_price = avg_price * 0.85
            elif conversion_rate > 0.8:
                recommendation = "raise_price"
                suggested_price = avg_price * 1.15
            else:
                recommendation = "maintain_price"
                suggested_price = avg_price
            
            return {
                "recommendation": recommendation,
                "current_avg_price": round(avg_price, 2),
                "suggested_price": round(suggested_price, 2),
                "conversion_rate": round(conversion_rate * 100, 1),
                "total_orders": total_orders
            }
        
        except Exception as e:
            logger.error(f"Pricing optimization failed: {e}")
            return {"recommendation": "error", "error": str(e)}
    
    def get_pricing_summary(self) -> Dict:
        """Get pricing summary for all services"""
        summary = {}
        
        for service_type in self.base_prices.keys():
            optimization = self.optimize_pricing(service_type)
            summary[service_type] = {
                "base_prices": self.base_prices[service_type],
                "optimization": optimization
            }
        
        return summary
