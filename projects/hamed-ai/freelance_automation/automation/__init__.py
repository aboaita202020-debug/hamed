"""
Automation Module - 24/7 Auto-Processing
"""
from .auto_processor import AutoProcessor
from .platform_monitor import PlatformMonitor
from .auto_analyzer import AutoAnalyzer
from .message_sender import MessageSender

__all__ = ['AutoProcessor', 'PlatformMonitor', 'AutoAnalyzer', 'MessageSender']
