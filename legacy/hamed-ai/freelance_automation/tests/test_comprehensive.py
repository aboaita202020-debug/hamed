"""
Comprehensive Tests for Hamed AI System
"""
import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.database import Database
from ai_brains.brain_router import BrainRouter
from sales.smart_sales_db import SmartSalesDatabase
from sales.smart_sales_agent import SmartSalesAgent
from calls.call_database import CallDatabase
from calls.call_manager import CallManager
from responses.professional_responses import ProfessionalResponseDB
from responses.messaging_integration import MessagingIntegration
from learning.web_learning import WebLearningDB
from social.social_media_manager import SocialMediaDB
from ai.advanced_ai_brain import AdvancedAIBrain

class TestCoreSystem(unittest.TestCase):
    """Test Core System Components"""
    
    def test_config_loads(self):
        """Test configuration loads successfully"""
        self.assertIsNotNone(Config.AI_BRAINS)
        self.assertEqual(len(Config.AI_BRAINS), 6)
    
    def test_database_initialization(self):
        """Test database initializes correctly"""
        db = Database()
        self.assertIsNotNone(db)
    
    def test_brain_router(self):
        """Test brain router functionality"""
        router = BrainRouter()
        self.assertIsNotNone(router)
        
        # Test brain selection
        brain_id = router._select_brain("content")
        self.assertIsNotNone(brain_id)

class TestSmartSales(unittest.TestCase):
    """Test Smart Sales System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = SmartSalesDatabase()
        self.agent = SmartSalesAgent()
    
    def test_register_service_type(self):
        """Test registering service type"""
        service_id = self.db.register_service_type(
            name='test_service',
            category='test',
            base_price=100.0
        )
        self.assertIsNotNone(service_id)
    
    def test_add_strategy(self):
        """Test adding sales strategy"""
        strategy_id = self.db.add_strategy(
            service_type='test_service',
            strategy_name='Test Strategy',
            approach='Test approach'
        )
        self.assertIsNotNone(strategy_id)
    
    def test_analyze_service_request(self):
        """Test analyzing service request"""
        analysis = self.agent.analyze_service_request('website_analysis')
        self.assertIsNotNone(analysis)
        self.assertIn('recommended_strategy', analysis)

class TestCallSystem(unittest.TestCase):
    """Test Call System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = CallDatabase()
        self.manager = CallManager()
    
    def test_add_contact(self):
        """Test adding contact"""
        contact_id = self.db.add_contact(
            name='Test Client',
            phone='01012345678',
            email='test@example.com'
        )
        self.assertIsNotNone(contact_id)
    
    def test_initiate_call(self):
        """Test initiating call"""
        call = self.manager.initiate_call(
            client_data={'name': 'Test', 'phone': '01012345678'},
            call_type='sales'
        )
        self.assertIsNotNone(call)
        self.assertIn('call_id', call)

class TestResponses(unittest.TestCase):
    """Test Response System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = ProfessionalResponseDB()
        self.messaging = MessagingIntegration()
    
    def test_get_response(self):
        """Test getting response"""
        response = self.db.get_response('greeting')
        self.assertIsNotNone(response)
    
    def test_detect_intent(self):
        """Test intent detection"""
        intent = self.messaging.detect_intent('مرحبا')
        self.assertIsNotNone(intent)
        self.assertEqual(intent['intent'], 'greeting')
    
    def test_process_message(self):
        """Test message processing"""
        response = self.messaging.process_message(
            client_id='test_client',
            platform='whatsapp',
            message='كم سعر خدمة تحليل الموقع؟'
        )
        self.assertIsNotNone(response)

class TestLearning(unittest.TestCase):
    """Test Learning System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = WebLearningDB()
    
    def test_add_knowledge(self):
        """Test adding knowledge"""
        knowledge_id = self.db.add_knowledge(
            category='test',
            topic='Test Topic',
            content='Test Content'
        )
        self.assertIsNotNone(knowledge_id)
    
    def test_get_knowledge(self):
        """Test getting knowledge"""
        knowledge = self.db.get_knowledge(category='marketing')
        self.assertIsNotNone(knowledge)

class TestSocialMedia(unittest.TestCase):
    """Test Social Media System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = SocialMediaDB()
    
    def test_add_account(self):
        """Test adding social account"""
        account_id = self.db.add_account(
            platform='instagram',
            username='test_account',
            account_type='business'
        )
        self.assertIsNotNone(account_id)
    
    def test_generate_content(self):
        """Test generating content"""
        content = self.db.generate_content(category='educational')
        self.assertIsNotNone(content)

class TestAdvancedAI(unittest.TestCase):
    """Test Advanced AI Brain"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ai_brain = AdvancedAIBrain()
    
    def test_think_and_generate_ideas(self):
        """Test idea generation"""
        client_context = {
            'type': 'business',
            'industry': 'ecommerce',
            'budget': 'medium',
            'goals': ['increase_sales']
        }
        ideas = self.ai_brain.think_and_generate_ideas(client_context)
        self.assertIsNotNone(ideas)
        self.assertGreater(len(ideas), 0)
    
    def test_negotiate_autonomously(self):
        """Test autonomous negotiation"""
        negotiation = self.ai_brain.negotiate_autonomously(
            client_id='test_client',
            service_type='website_analysis',
            client_budget=100,
            client_requirements={'complexity': 'medium'}
        )
        self.assertIsNotNone(negotiation)
        self.assertIn('final_price', negotiation)
    
    def test_make_autonomous_decision(self):
        """Test autonomous decision making"""
        decision = self.ai_brain.make_autonomous_decision({
            'type': 'pricing',
            'urgency': 'high',
            'risk': 'low',
            'value': 2000
        })
        self.assertIsNotNone(decision)
        self.assertIn('action', decision)
    
    def test_create_proposal(self):
        """Test proposal creation"""
        proposal = self.ai_brain.create_proposal(
            client_id='test_client',
            service_type='seo_optimization',
            client_requirements={
                'complexity': 'high',
                'budget': 'high'
            }
        )
        self.assertIsNotNone(proposal)
        self.assertIn('proposal_text', proposal)

class TestIntegration(unittest.TestCase):
    """Integration Tests"""
    
    def test_full_sales_flow(self):
        """Test complete sales flow"""
        # 1. Initialize systems
        sales_agent = SmartSalesAgent()
        ai_brain = AdvancedAIBrain()
        
        # 2. Analyze client
        analysis = sales_agent.analyze_service_request('website_analysis')
        self.assertIsNotNone(analysis)
        
        # 3. Generate ideas
        ideas = ai_brain.think_and_generate_ideas({
            'type': 'business',
            'industry': 'ecommerce'
        })
        self.assertGreater(len(ideas), 0)
        
        # 4. Create proposal
        proposal = ai_brain.create_proposal(
            client_id='integration_test',
            service_type='website_analysis',
            client_requirements={'complexity': 'medium'}
        )
        self.assertIsNotNone(proposal)
    
    def test_full_negotiation_flow(self):
        """Test complete negotiation flow"""
        ai_brain = AdvancedAIBrain()
        
        # Negotiate
        negotiation = ai_brain.negotiate_autonomously(
            client_id='test_client',
            service_type='seo_optimization',
            client_budget=200,
            client_requirements={'complexity': 'high'}
        )
        
        # Verify
        self.assertIsNotNone(negotiation)
        self.assertIn('final_price', negotiation)
        self.assertGreater(negotiation['final_price'], 0)

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
