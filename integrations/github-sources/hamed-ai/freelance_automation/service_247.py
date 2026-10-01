"""
24/7 Service - Main daemon that runs all automation
"""
import sys
import time
import signal
import threading
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.database import Database
from core.logger import logger
from automation.auto_processor import AutoProcessor
from automation.platform_monitor import PlatformMonitor

class Service247:
    """Main 24/7 service daemon"""
    
    def __init__(self):
        self.db = Database()
        self.auto_processor = AutoProcessor(check_interval=60)  # Check every minute
        self.platform_monitor = PlatformMonitor(check_interval=300)  # Check platforms every 5 min
        self.running = False
        self.start_time = None
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def start(self):
        """Start the 24/7 service"""
        logger.info("=" * 60)
        logger.info("🤖 FREELANCE AUTOMATION 24/7 SERVICE")
        logger.info("=" * 60)
        logger.info(f"Started at: {datetime.now().isoformat()}")
        logger.info(f"Auto-processor: checks every {self.auto_processor.check_interval}s")
        logger.info(f"Platform monitor: checks every {self.platform_monitor.check_interval}s")
        logger.info("=" * 60)
        
        self.running = True
        self.start_time = datetime.now()
        
        # Start auto-processor
        self.auto_processor.start()
        logger.info("✓ Auto-processor started")
        
        # Start platform monitor
        self.platform_monitor.start()
        logger.info("✓ Platform monitor started")
        
        # Main loop - keep service alive
        try:
            while self.running:
                self._heartbeat()
                time.sleep(60)  # Heartbeat every minute
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the 24/7 service"""
        if not self.running:
            return
        
        logger.info("Stopping 24/7 service...")
        self.running = False
        
        # Stop components
        self.auto_processor.stop()
        self.platform_monitor.stop()
        
        # Log final stats
        if self.start_time:
            uptime = datetime.now() - self.start_time
            logger.info(f"Service uptime: {uptime}")
        
        logger.info("Service stopped gracefully")
    
    def _heartbeat(self):
        """Log heartbeat with stats"""
        try:
            # Get current stats
            pending = self.db.fetch_one("SELECT COUNT(*) as count FROM orders WHERE status = 'pending'")
            in_progress = self.db.fetch_one("SELECT COUNT(*) as count FROM orders WHERE status = 'in_progress'")
            revenue = self.db.get_revenue_summary(days=1)
            
            logger.info(
                f"💓 Heartbeat | "
                f"Pending: {pending['count'] if pending else 0} | "
                f"In Progress: {in_progress['count'] if in_progress else 0} | "
                f"Revenue (24h): ${revenue['total_revenue']:.2f}"
            )
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
    
    def get_status(self) -> Dict:
        """Get service status"""
        uptime = datetime.now() - self.start_time if self.start_time else None
        
        return {
            "running": self.running,
            "uptime": str(uptime) if uptime else "N/A",
            "auto_processor": self.auto_processor.get_status(),
            "platform_monitor": self.platform_monitor.get_status()
        }

def main():
    """Main entry point for 24/7 service"""
    print("\n" + "=" * 60)
    print("🤖 FREELANCE AUTOMATION 24/7 SERVICE")
    print("=" * 60)
    print()
    print("This service will run continuously and:")
    print("  • Monitor platforms for new orders")
    print("  • Process orders automatically with AI")
    print("  • Deliver completed orders")
    print("  • Track revenue 24/7")
    print()
    print("Press Ctrl+C to stop the service")
    print("=" * 60)
    print()
    
    # Validate config first
    errors = Config.validate()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print()
        print("Please fix .env file and try again")
        sys.exit(1)
    
    print("✓ Configuration validated")
    print()
    
    # Start service
    service = Service247()
    service.start()

if __name__ == "__main__":
    main()
