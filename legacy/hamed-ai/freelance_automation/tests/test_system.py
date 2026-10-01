"""
Tests for Freelance Automation System
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.database import Database
from ai_brains.brain_router import BrainRouter

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_config_loads(self):
        """Test config loads without errors"""
        self.assertIsNotNone(Config.AI_BRAINS)
        self.assertEqual(len(Config.AI_BRAINS), 6)
    
    def test_config_has_required_brains(self):
        """Test all 6 brains are configured"""
        required_brains = ['brain_1', 'brain_2', 'brain_3', 'brain_4', 'brain_5', 'brain_6']
        for brain_id in required_brains:
            self.assertIn(brain_id, Config.AI_BRAINS)
    
    def test_config_services(self):
        """Test services are configured"""
        self.assertIn('content_writing', Config.SERVICES)
        self.assertIn('translation', Config.SERVICES)
        self.assertIn('data_analysis', Config.SERVICES)
        self.assertIn('code_generation', Config.SERVICES)

class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.db = Database()
    
    def test_database_initialization(self):
        """Test database initializes correctly"""
        self.assertIsNotNone(self.db)
    
    def test_create_order(self):
        """Test order creation"""
        order_data = {
            "platform": "fiverr",
            "service_type": "content_writing",
            "client_name": "Test Client",
            "description": "Test order",
            "price": 10.0
        }
        
        order_id = self.db.create_order(order_data)
        self.assertIsNotNone(order_id)
        self.assertTrue(order_id.startswith("ORD-"))
    
    def test_get_order(self):
        """Test getting order"""
        order_data = {
            "platform": "upwork",
            "service_type": "translation",
            "client_name": "Test Client 2",
            "description": "Test order 2",
            "price": 5.0
        }
        
        order_id = self.db.create_order(order_data)
        order = self.db.get_order(order_id)
        
        self.assertIsNotNone(order)
        self.assertEqual(order['id'], order_id)
        self.assertEqual(order['client_name'], "Test Client 2")
    
    def test_update_order_status(self):
        """Test updating order status"""
        order_data = {
            "platform": "mostaql",
            "service_type": "data_analysis",
            "client_name": "Test Client 3",
            "description": "Test order 3",
            "price": 20.0
        }
        
        order_id = self.db.create_order(order_data)
        self.db.update_order_status(order_id, "in_progress")
        
        order = self.db.get_order(order_id)
        self.assertEqual(order['status'], "in_progress")
    
    def test_get_brain_stats(self):
        """Test getting brain stats"""
        stats = self.db.fetch_all("SELECT * FROM brains")
        self.assertEqual(len(stats), 6)

class TestBrainRouter(unittest.TestCase):
    """Test brain router"""
    
    def setUp(self):
        """Set up brain router"""
        self.router = BrainRouter()
    
    def test_router_initialization(self):
        """Test router initializes"""
        self.assertIsNotNone(self.router)
    
    def test_select_brain_content(self):
        """Test selecting brain for content task"""
        brain_id = self.router._select_brain("content")
        self.assertIsNotNone(brain_id)
    
    def test_select_brain_translation(self):
        """Test selecting brain for translation task"""
        brain_id = self.router._select_brain("translation")
        self.assertIsNotNone(brain_id)
    
    def test_get_brain_stats(self):
        """Test getting brain statistics"""
        stats = self.router.get_brain_stats()
        self.assertEqual(len(stats), 6)
    
    def test_health_check(self):
        """Test health check"""
        health = self.router.health_check()
        self.assertEqual(len(health), 6)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_order_flow(self):
        """Test complete order flow"""
        db = Database()
        router = BrainRouter()
        
        # Create order
        order_data = {
            "platform": "fiverr",
            "service_type": "content_writing",
            "client_name": "Integration Test Client",
            "description": "Write a blog post about AI",
            "price": 15.0
        }
        
        order_id = db.create_order(order_data)
        
        # Process order
        db.update_order_status(order_id, "in_progress")
        
        payload = {
            "instruction": "Write a blog post about AI",
            "requirements": {"length": "1000 words", "tone": "professional"},
            "client_name": "Integration Test Client",
            "order_id": order_id
        }
        
        result = router.route_task("content", payload)
        
        # Update order
        if result['success']:
            db.update_order_status(order_id, "completed", 
                                 assigned_brain=result['brain_id'],
                                 result=result['result'])
        
        # Verify
        order = db.get_order(order_id)
        self.assertEqual(order['status'], "completed")

if __name__ == '__main__':
    unittest.main()
