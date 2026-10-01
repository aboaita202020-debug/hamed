"""
Logging System - Asynchronous, non-blocking
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import threading
import queue

from .config import Config

class AsyncLogger:
    """Asynchronous logger with queue-based processing"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize logger"""
        if self._initialized:
            return
        
        self.logger = logging.getLogger('freelance_automation')
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Async queue
        self.log_queue = queue.Queue()
        self._start_async_processor()
        
        self._initialized = True
    
    def _start_async_processor(self):
        """Start async log processor thread"""
        def processor():
            while True:
                try:
                    log_func, message, kwargs = self.log_queue.get()
                    if log_func is None:
                        break
                    log_func(message, **kwargs)
                except Exception as e:
                    print(f"Logger error: {e}", file=sys.stderr)
        
        thread = threading.Thread(target=processor, daemon=True)
        thread.start()
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.log_queue.put((self.logger.info, message, kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.log_queue.put((self.logger.warning, message, kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.log_queue.put((self.logger.error, message, kwargs))
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.log_queue.put((self.logger.debug, message, kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.log_queue.put((self.logger.critical, message, kwargs))
    
    def task_start(self, task_id: str, task_type: str, **kwargs):
        """Log task start"""
        self.info(f"Task started: {task_id} ({task_type})", extra=kwargs)
    
    def task_complete(self, task_id: str, task_type: str, duration: float, **kwargs):
        """Log task completion"""
        self.info(f"Task completed: {task_id} ({task_type}) in {duration:.2f}s", extra=kwargs)
    
    def task_error(self, task_id: str, task_type: str, error: str, **kwargs):
        """Log task error"""
        self.error(f"Task failed: {task_id} ({task_type}) - {error}", extra=kwargs)
    
    def api_call(self, brain_id: str, endpoint: str, duration: float, success: bool):
        """Log API call"""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"API call to {brain_id}: {endpoint} - {status} ({duration:.2f}s)")
    
    def order_event(self, order_id: str, event: str, **kwargs):
        """Log order event"""
        self.info(f"Order {order_id}: {event}", extra=kwargs)
    
    def revenue_event(self, amount: float, order_id: str, service_type: str):
        """Log revenue event"""
        self.info(f"Revenue recorded: ${amount:.2f} from {service_type} (Order: {order_id})")

# Global logger instance
logger = AsyncLogger()
