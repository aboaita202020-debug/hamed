"""
Platform Monitor - Monitors freelance platforms for new orders
"""
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional

from core.config import Config
from core.database import Database
from core.logger import logger

class PlatformMonitor:
    """Monitors platforms for new orders automatically"""
    
    def __init__(self, check_interval: int = 300):
        """
        Initialize platform monitor
        
        Args:
            check_interval: Seconds between platform checks (default: 5 minutes)
        """
        self.db = Database()
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        
        logger.info(f"PlatformMonitor initialized (check every {check_interval}s)")
    
    def start(self):
        """Start monitoring in background thread"""
        if self.running:
            logger.warning("PlatformMonitor already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        logger.info("PlatformMonitor started - watching platforms 24/7")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        
        logger.info("PlatformMonitor stopped")
    
    def _run_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                self._check_platforms()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"PlatformMonitor error: {e}")
                time.sleep(60)
    
    def _check_platforms(self):
        """Check all platforms for new orders"""
        platforms = ['fiverr', 'upwork', 'mostaql']
        
        for platform in platforms:
            try:
                self._check_platform(platform)
            except Exception as e:
                logger.error(f"Error checking {platform}: {e}")
    
    def _check_platform(self, platform: str):
        """Check single platform for new orders"""
        # TODO: Implement actual platform API integration
        # For now, this is a placeholder
        
        logger.debug(f"Checking {platform} for new orders...")
        
        # Mock: Simulate checking platform
        # In production, this would call platform APIs:
        # - Fiverr API: GET /buyer/requests
        # - Upwork API: GET /jobs
        # - Mostaql API: GET /projects
        
        # Example implementation (commented):
        # if platform == 'fiverr':
        #     orders = self._check_fiverr()
        # elif platform == 'upwork':
        #     orders = self._check_upwork()
        # elif platform == 'mostaql':
        #     orders = self._check_mostaql()
        
        # for order in orders:
        #     self._create_order_from_platform(platform, order)
    
    def _check_fiverr(self) -> List[Dict]:
        """Check Fiverr for new orders"""
        # TODO: Implement Fiverr API integration
        # API Key needed: Config.FIVERR_API_KEY
        return []
    
    def _check_upwork(self) -> List[Dict]:
        """Check Upwork for new orders"""
        # TODO: Implement Upwork API integration
        # API Key needed: Config.UPWORK_API_KEY
        return []
    
    def _check_mostaql(self) -> List[Dict]:
        """Check Mostaql for new orders"""
        # TODO: Implement Mostaql API integration
        # API Key needed: Config.MOSTAQL_API_KEY
        return []
    
    def _create_order_from_platform(self, platform: str, order_data: Dict):
        """Create order from platform data"""
        try:
            # Check if order already exists
            existing = self.db.fetch_one(
                "SELECT id FROM orders WHERE platform = ? AND client_name = ? AND created_at > ?",
                (platform, order_data.get('client_name'), 
                 (datetime.now() - timedelta(hours=1)).isoformat())
            )
            
            if existing:
                logger.debug(f"Order already exists: {existing['id']}")
                return
            
            # Create new order
            order_id = self.db.create_order({
                "platform": platform,
                "service_type": order_data.get('service_type', 'content_writing'),
                "client_name": order_data.get('client_name', 'Unknown'),
                "client_email": order_data.get('client_email', ''),
                "description": order_data.get('description', ''),
                "requirements": order_data.get('requirements', {}),
                "price": order_data.get('price', 0.0)
            })
            
            logger.info(f"New order from {platform}: {order_id}")
            
        except Exception as e:
            logger.error(f"Failed to create order from {platform}: {e}")
    
    def get_status(self) -> Dict:
        """Get monitor status"""
        return {
            "running": self.running,
            "check_interval": self.check_interval,
            "thread_alive": self.thread.is_alive() if self.thread else False
        }
