"""
Freelance Automation System
"""
__version__ = "1.0.0"
__author__ = "Hamed AI"

from .core import Config, Database, logger
from .ai_brains import BrainRouter

__all__ = ['Config', 'Database', 'logger', 'BrainRouter']
