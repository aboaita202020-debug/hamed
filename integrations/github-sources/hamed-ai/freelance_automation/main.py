#!/usr/bin/env python3
"""
Freelance Automation System - Main CLI Interface
"""
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.database import Database
from core.logger import logger
from ai_brains.brain_router import BrainRouter

class FreelanceAutomation:
    """Main application class"""
    
    def __init__(self):
        self.db = Database()
        self.brain_router = BrainRouter()
        logger.info("Freelance Automation System initialized")
    
    def create_order(self, platform: str, service_type: str, client_name: str, 
                     description: str, price: float, **kwargs) -> str:
        """Create new order"""
        order_data = {
            "platform": platform,
            "service_type": service_type,
            "client_name": client_name,
            "description": description,
            "price": price,
            **kwargs
        }
        
        order_id = self.db.create_order(order_data)
        logger.order_event(order_id, "created", platform=platform, service_type=service_type)
        
        return order_id
    
    def process_order(self, order_id: str) -> Dict:
        """Process order with AI brain"""
        order = self.db.get_order(order_id)
        if not order:
            raise ValueError(f"Order not found: {order_id}")
        
        # Map service type to task type
        task_type_map = {
            "content_writing": "content",
            "translation": "translation",
            "data_analysis": "analysis",
            "code_generation": "code"
        }
        
        task_type = task_type_map.get(order['service_type'])
        if not task_type:
            raise ValueError(f"Unknown service type: {order['service_type']}")
        
        # Update order status
        self.db.update_order_status(order_id, "in_progress")
        
        # Prepare payload for brain
        payload = {
            "instruction": order['description'],
            "requirements": json.loads(order['requirements']) if order['requirements'] else {},
            "client_name": order['client_name'],
            "order_id": order_id
        }
        
        # Route to brain
        result = self.brain_router.route_task(task_type, payload)
        
        if result['success']:
            self.db.update_order_status(
                order_id, 
                "completed",
                assigned_brain=result['brain_id'],
                result=result['result'],
                quality_score=100.0  # TODO: Implement quality checking
            )
            logger.order_event(order_id, "completed", brain_id=result['brain_id'])
        else:
            self.db.update_order_status(order_id, "failed")
            logger.order_event(order_id, "failed", error=result.get('error'))
        
        return result
    
    def deliver_order(self, order_id: str):
        """Mark order as delivered"""
        order = self.db.get_order(order_id)
        if not order:
            raise ValueError(f"Order not found: {order_id}")
        
        if order['status'] != 'completed':
            raise ValueError(f"Order must be completed before delivery: {order['status']}")
        
        self.db.update_order_status(order_id, "delivered")
        
        # Record revenue
        self.db.record_revenue(
            order_id=order_id,
            amount=order['price'],
            platform=order['platform'],
            service_type=order['service_type']
        )
        
        logger.order_event(order_id, "delivered")
        logger.revenue_event(order['price'], order_id, order['service_type'])
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        # Revenue summary
        revenue = self.db.get_revenue_summary(days=30)
        
        # Orders summary
        total_orders = self.db.fetch_one("SELECT COUNT(*) as count FROM orders")
        pending_orders = self.db.fetch_one("SELECT COUNT(*) as count FROM orders WHERE status = 'pending'")
        completed_orders = self.db.fetch_one("SELECT COUNT(*) as count FROM orders WHERE status = 'completed'")
        delivered_orders = self.db.fetch_one("SELECT COUNT(*) as count FROM orders WHERE status = 'delivered'")
        
        # Brain stats
        brain_stats = self.brain_router.get_brain_stats()
        
        return {
            "revenue": revenue,
            "orders": {
                "total": total_orders['count'] if total_orders else 0,
                "pending": pending_orders['count'] if pending_orders else 0,
                "completed": completed_orders['count'] if completed_orders else 0,
                "delivered": delivered_orders['count'] if delivered_orders else 0
            },
            "brains": brain_stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        errors = Config.validate()
        
        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        logger.info("Configuration validation passed")
        return True

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Freelance Automation System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configuration")
    
    # Create order command
    create_parser = subparsers.add_parser("create-order", help="Create new order")
    create_parser.add_argument("--platform", required=True, help="Platform (fiverr, upwork, mostaql)")
    create_parser.add_argument("--service", required=True, help="Service type")
    create_parser.add_argument("--client", required=True, help="Client name")
    create_parser.add_argument("--description", required=True, help="Order description")
    create_parser.add_argument("--price", type=float, required=True, help="Order price")
    
    # Process order command
    process_parser = subparsers.add_parser("process-order", help="Process order with AI")
    process_parser.add_argument("order_id", help="Order ID to process")
    
    # Deliver order command
    deliver_parser = subparsers.add_parser("deliver-order", help="Mark order as delivered")
    deliver_parser.add_argument("order_id", help="Order ID to deliver")
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Show dashboard stats")
    
    # Brain stats command
    brains_parser = subparsers.add_parser("brains", help="Show brain statistics")
    
    # 24/7 Service command
    service_parser = subparsers.add_parser("service", help="Start 24/7 auto-processing service")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize application
    app = FreelanceAutomation()
    
    try:
        if args.command == "validate":
            success = app.validate_config()
            sys.exit(0 if success else 1)
        
        elif args.command == "create-order":
            order_id = app.create_order(
                platform=args.platform,
                service_type=args.service,
                client_name=args.client,
                description=args.description,
                price=args.price
            )
            print(f"✓ Order created: {order_id}")
        
        elif args.command == "process-order":
            result = app.process_order(args.order_id)
            if result['success']:
                print(f"✓ Order processed successfully")
                print(f"  Brain: {result['brain_name']}")
                print(f"  Duration: {result['duration']:.2f}s")
            else:
                print(f"✗ Order processing failed: {result.get('error')}")
                sys.exit(1)
        
        elif args.command == "deliver-order":
            app.deliver_order(args.order_id)
            print(f"✓ Order delivered: {args.order_id}")
        
        elif args.command == "dashboard":
            stats = app.get_dashboard_stats()
            print("\n=== FREELANCE AUTOMATION DASHBOARD ===\n")
            print(f"Revenue (30 days): ${stats['revenue']['total_revenue']:.2f}")
            print(f"Total Orders: {stats['orders']['total']}")
            print(f"  - Pending: {stats['orders']['pending']}")
            print(f"  - Completed: {stats['orders']['completed']}")
            print(f"  - Delivered: {stats['orders']['delivered']}")
            print(f"\nAI Brains:")
            for brain_id, brain in stats['brains'].items():
                print(f"  {brain['name']}: {brain['successful_tasks']}/{brain['total_tasks']} tasks ({brain['success_rate']:.1f}% success)")
            print()
        
        elif args.command == "brains":
            stats = app.brain_router.get_brain_stats()
            print("\n=== AI BRAINS STATUS ===\n")
            for brain_id, brain in stats.items():
                print(f"{brain['name']} ({brain_id})")
                print(f"  Specialty: {brain['specialty']}")
                print(f"  Status: {brain['status']}")
                print(f"  Tasks: {brain['successful_tasks']}/{brain['total_tasks']} successful")
                print(f"  Success Rate: {brain['success_rate']:.1f}%")
                print(f"  Avg Response Time: {brain['avg_response_time']:.2f}s")
                print()
        
        elif args.command == "service":
            print("\n🤖 Starting 24/7 Auto-Processing Service...")
            print("Press Ctrl+C to stop\n")
            from service_247 import Service247
            service = Service247()
            service.start()
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
