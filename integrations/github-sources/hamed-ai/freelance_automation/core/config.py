"""
Core Configuration - Freelance Automation System
"""
import os
from pathlib import Path

class Config:
    """Configuration manager with environment variables"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Create directories
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Database
    DB_PATH = DATA_DIR / "freelance.db"
    
    # AI Brains Configuration (6 brains)
    AI_BRAINS = {
        "brain_1": {
            "name": os.getenv("BRAIN_1_NAME", "Content Writer"),
            "provider": os.getenv("BRAIN_1_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_1_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_1_API_KEY", ""),
            "specialty": "content_creation"
        },
        "brain_2": {
            "name": os.getenv("BRAIN_2_NAME", "Translator"),
            "provider": os.getenv("BRAIN_2_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_2_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_2_API_KEY", ""),
            "specialty": "translation"
        },
        "brain_3": {
            "name": os.getenv("BRAIN_3_NAME", "Data Analyst"),
            "provider": os.getenv("BRAIN_3_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_3_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_3_API_KEY", ""),
            "specialty": "analysis"
        },
        "brain_4": {
            "name": os.getenv("BRAIN_4_NAME", "Code Generator"),
            "provider": os.getenv("BRAIN_4_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_4_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_4_API_KEY", ""),
            "specialty": "coding"
        },
        "brain_5": {
            "name": os.getenv("BRAIN_5_NAME", "Quality Checker"),
            "provider": os.getenv("BRAIN_5_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_5_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_5_API_KEY", ""),
            "specialty": "quality"
        },
        "brain_6": {
            "name": os.getenv("BRAIN_6_NAME", "Optimizer"),
            "provider": os.getenv("BRAIN_6_PROVIDER", "anthropic"),
            "model": os.getenv("BRAIN_6_MODEL", "claude-3-5-sonnet-20241022"),
            "api_key": os.getenv("BRAIN_6_API_KEY", ""),
            "specialty": "optimization"
        }
    }
    
    # Services Configuration
    SERVICES = {
        "content_writing": {
            "enabled": True,
            "base_price": 10,  # USD
            "brain": "brain_1"
        },
        "translation": {
            "enabled": True,
            "base_price": 5,
            "brain": "brain_2"
        },
        "data_analysis": {
            "enabled": True,
            "base_price": 20,
            "brain": "brain_3"
        },
        "code_generation": {
            "enabled": True,
            "base_price": 15,
            "brain": "brain_4"
        }
    }
    
    # Platforms Configuration
    PLATFORMS = {
        "fiverr": {
            "enabled": True,
            "api_url": "https://www.fiverr.com/api/v1",
            "api_key": os.getenv("FIVERR_API_KEY", "")
        },
        "upwork": {
            "enabled": True,
            "api_url": "https://api.upwork.com/v1",
            "api_key": os.getenv("UPWORK_API_KEY", "")
        },
        "mostaql": {
            "enabled": True,
            "api_url": "https://mostaql.com/api/v1",
            "api_key": os.getenv("MOSTAQL_API_KEY", "")
        }
    }
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "freelance.log"
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        # Check AI brains
        for brain_id, brain in cls.AI_BRAINS.items():
            if not brain["api_key"]:
                errors.append(f"Missing API key for {brain['name']} ({brain_id})")
        
        # Check platforms
        for platform_id, platform in cls.PLATFORMS.items():
            if platform["enabled"] and not platform["api_key"]:
                errors.append(f"Missing API key for {platform_id}")
        
        return errors
    
    @classmethod
    def get_brain(cls, brain_id):
        """Get brain configuration by ID"""
        return cls.AI_BRAINS.get(brain_id)
    
    @classmethod
    def get_service_config(cls, service_name):
        """Get service configuration by name"""
        return cls.SERVICES.get(service_name)
