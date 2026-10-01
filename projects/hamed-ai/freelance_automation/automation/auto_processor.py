"""
Auto-Processor - Monitors and processes orders automatically 24/7
"""
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from core.config import Config
from core.database import Database
from core.logger import logger
from ai_brains.brain_router import BrainRouter

class AutoProcessor:
    """Automatic order processor - runs 24/7"""
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize auto-processor
        
        Args:
            check_interval: Seconds between checks (default: 60)
        """
        self.db = Database()
        self.brain_router = BrainRouter()
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        
        logger.info(f"AutoProcessor initialized (check every {check_interval}s)")
    
    def start(self):
        """Start auto-processing in background thread"""
        if self.running:
            logger.warning("AutoProcessor already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        logger.info("AutoProcessor started - monitoring orders 24/7")
    
    def stop(self):
        """Stop auto-processing"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        
        logger.info("AutoProcessor stopped")
    
    def _run_loop(self):
        """Main processing loop"""
        while self.running:
            try:
                self._process_cycle()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"AutoProcessor error: {e}")
                time.sleep(30)  # Wait before retry
    
    def _process_cycle(self):
        """Single processing cycle - optimized for performance"""
        start_time = time.time()
        
        # 1. Get pending orders (batch for efficiency)
        pending_orders = self.db.get_pending_orders()
        
        if not pending_orders:
            logger.debug("No pending orders")
            return
        
        # 2. Sort by priority (price desc = higher priority)
        pending_orders.sort(key=lambda x: x.get('price', 0), reverse=True)
        
        logger.info(f"Processing {len(pending_orders)} pending orders (priority sorted)")
        
        # 3. Process orders in batches
        processed_count = 0
        failed_count = 0
        
        for order in pending_orders:
            try:
                self._process_order(order)
                processed_count += 1
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to process order {order['id']}: {e}")
        
        # 4. Log cycle performance
        cycle_duration = time.time() - start_time
        logger.info(
            f"Cycle completed: {processed_count} processed, {failed_count} failed "
            f"in {cycle_duration:.2f}s"
        )
    
    def _process_order(self, order: Dict):
        """Process single order"""
        order_id = order['id']
        service_type = order['service_type']
        
        logger.order_event(order_id, "auto-processing started")
        
        # Map service to task type
        task_type_map = {
            "content_writing": "content",
            "translation": "translation",
            "data_analysis": "analysis",
            "code_generation": "code"
        }
        
        task_type = task_type_map.get(service_type)
        if not task_type:
            logger.error(f"Unknown service type: {service_type}")
            self.db.update_order_status(order_id, "failed")
            return
        
        # Update status
        self.db.update_order_status(order_id, "in_progress")
        
        # Prepare payload
        payload = {
            "instruction": order['description'],
            "requirements": json.loads(order['requirements']) if order['requirements'] else {},
            "client_name": order['client_name'],
            "order_id": order_id
        }
        
        # Route to brain
        result = self.brain_router.route_task(task_type, payload)
        
        if result['success']:
            # Update order with result
            self.db.update_order_status(
                order_id,
                "completed",
                assigned_brain=result['brain_id'],
                result=result['result'],
                quality_score=100.0
            )
            
            logger.order_event(order_id, "auto-processed successfully", 
                             brain_id=result['brain_id'],
                             duration=result['duration'])
            
            # Auto-deliver after processing
            self._auto_deliver(order_id)
        else:
            self.db.update_order_status(order_id, "failed")
            logger.order_event(order_id, "auto-processing failed", 
                             error=result.get('error'))
    
    def _auto_deliver(self, order_id: str):
        """Automatically deliver completed order"""
        try:
            order = self.db.get_order(order_id)
            if not order or order['status'] != 'completed':
                return
            
            # Mark as delivered
            self.db.update_order_status(order_id, "delivered")
            
            # Record revenue
            self.db.record_revenue(
                order_id=order_id,
                amount=order['price'],
                platform=order['platform'],
                service_type=order['service_type']
            )
            
            logger.order_event(order_id, "auto-delivered")
            logger.revenue_event(order['price'], order_id, order['service_type'])
            
        except Exception as e:
            logger.error(f"Auto-delivery failed for {order_id}: {e}")
    
    def get_status(self) -> Dict:
        """Get auto-processor status"""
        return {
            "running": self.running,
            "check_interval": self.check_interval,
            "thread_alive": self.thread.is_alive() if self.thread else False
        }
