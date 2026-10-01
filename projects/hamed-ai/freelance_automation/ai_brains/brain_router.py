"""
AI Brain Router - Distributes tasks to 6 AI brains
"""
import time
import json
from typing import Dict, Any, Optional
from datetime import datetime

from core.config import Config
from core.database import Database
from core.logger import logger

class BrainRouter:
    """Routes tasks to appropriate AI brains"""
    
    def __init__(self):
        self.db = Database()
        self.brains = Config.AI_BRAINS
    
    def route_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route task to appropriate brain based on task type
        
        Args:
            task_type: Type of task (content, translation, analysis, code, quality, optimization)
            payload: Task payload with instructions and context
        
        Returns:
            Dict with result, brain_id, duration, success status
        """
        start_time = time.time()
        task_id = f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
        
        logger.task_start(task_id, task_type)
        
        try:
            # Find appropriate brain
            brain_id = self._select_brain(task_type)
            if not brain_id:
                raise ValueError(f"No available brain for task type: {task_type}")
            
            brain_config = self.brains[brain_id]
            
            # Execute task with brain
            result = self._execute_with_brain(brain_id, brain_config, payload)
            
            duration = time.time() - start_time
            
            # Update brain stats
            self.db.update_brain_stats(brain_id, success=True, response_time=duration)
            
            logger.task_complete(task_id, task_type, duration)
            
            return {
                "task_id": task_id,
                "brain_id": brain_id,
                "brain_name": brain_config['name'],
                "result": result,
                "duration": duration,
                "success": True
            }
        
        except Exception as e:
            duration = time.time() - start_time
            logger.task_error(task_id, task_type, str(e))
            
            return {
                "task_id": task_id,
                "brain_id": None,
                "result": None,
                "error": str(e),
                "duration": duration,
                "success": False
            }
    
    def _select_brain(self, task_type: str) -> Optional[str]:
        """Select best brain for task type"""
        specialty_map = {
            "content": "content_creation",
            "translation": "translation",
            "analysis": "analysis",
            "code": "coding",
            "quality": "quality",
            "optimization": "optimization"
        }
        
        specialty = specialty_map.get(task_type)
        if not specialty:
            return None
        
        brain = self.db.get_available_brain(specialty)
        return brain['id'] if brain else None
    
    def _execute_with_brain(self, brain_id: str, brain_config: Dict, payload: Dict) -> Any:
        """
        Execute task with specific brain
        
        Note: This is a mock implementation. In production, integrate with actual AI APIs.
        """
        provider = brain_config['provider']
        model = brain_config['model']
        api_key = brain_config['api_key']
        
        start_time = time.time()
        
        try:
            # Mock API call (replace with actual API integration)
            result = self._mock_ai_call(provider, model, api_key, payload)
            
            duration = time.time() - start_time
            logger.api_call(brain_id, f"{provider}/{model}", duration, success=True)
            
            return result
        
        except Exception as e:
            duration = time.time() - start_time
            logger.api_call(brain_id, f"{provider}/{model}", duration, success=False)
            raise
    
    def _mock_ai_call(self, provider: str, model: str, api_key: str, payload: Dict) -> Dict:
        """
        Mock AI API call for testing
        
        Replace this with actual API integration:
        - Anthropic Claude API
        - OpenAI API
        - Google Gemini API
        - etc.
        """
        if not api_key:
            # Return mock response for testing
            return {
                "content": f"Mock response from {model} for task: {payload.get('instruction', 'N/A')}",
                "tokens_used": 100,
                "model": model,
                "provider": provider
            }
        
        # TODO: Implement actual API calls
        # Example for Anthropic Claude:
        # import anthropic
        # client = anthropic.Anthropic(api_key=api_key)
        # message = client.messages.create(
        #     model=model,
        #     max_tokens=1000,
        #     messages=[{"role": "user", "content": payload['instruction']}]
        # )
        # return {"content": message.content[0].text, "tokens_used": message.usage.output_tokens}
        
        raise NotImplementedError(f"API integration for {provider} not implemented yet")
    
    def get_brain_stats(self) -> Dict[str, Dict]:
        """Get statistics for all brains"""
        stats = {}
        
        for brain_id in self.brains:
            brain_data = self.db.fetch_one("SELECT * FROM brains WHERE id = ?", (brain_id,))
            if brain_data:
                stats[brain_id] = {
                    "name": brain_data['name'],
                    "specialty": brain_data['specialty'],
                    "status": brain_data['status'],
                    "total_tasks": brain_data['total_tasks'],
                    "successful_tasks": brain_data['successful_tasks'],
                    "failed_tasks": brain_data['failed_tasks'],
                    "success_rate": (brain_data['successful_tasks'] / brain_data['total_tasks'] * 100) 
                                   if brain_data['total_tasks'] > 0 else 0,
                    "avg_response_time": brain_data['avg_response_time'],
                    "last_used": brain_data['last_used']
                }
        
        return stats
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all brains"""
        health = {}
        
        for brain_id, brain_config in self.brains.items():
            # Check if API key is configured
            has_key = bool(brain_config['api_key'])
            
            # Check if brain is active in database
            brain_data = self.db.fetch_one("SELECT status FROM brains WHERE id = ?", (brain_id,))
            is_active = brain_data and brain_data['status'] == 'active'
            
            health[brain_id] = has_key and is_active
        
        return health
