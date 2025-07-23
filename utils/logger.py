import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """Centralized logging utility for the CV Assistant application"""
    
    def __init__(self, name: str = "cv_assistant", log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup logging handlers for console and file output"""
        
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        log_filename = f"{log_dir}/cv_assistant_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str, extra: Optional[dict] = None):
        """Log info message"""
        self.logger.info(message, extra=extra)
    
    def debug(self, message: str, extra: Optional[dict] = None):
        """Log debug message"""
        self.logger.debug(message, extra=extra)
    
    def warning(self, message: str, extra: Optional[dict] = None):
        """Log warning message"""
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, extra: Optional[dict] = None):
        """Log error message"""
        self.logger.error(message, extra=extra)
    
    def critical(self, message: str, extra: Optional[dict] = None):
        """Log critical message"""
        self.logger.critical(message, extra=extra)
    
    def log_agent_start(self, agent_name: str, task: str):
        """Log when an agent starts a task"""
        self.info(f"Agent '{agent_name}' started task: {task}")
    
    def log_agent_complete(self, agent_name: str, task: str, duration: float):
        """Log when an agent completes a task"""
        self.info(f"Agent '{agent_name}' completed task: {task} (Duration: {duration:.2f}s)")
    
    def log_agent_error(self, agent_name: str, task: str, error: str):
        """Log when an agent encounters an error"""
        self.error(f"Agent '{agent_name}' error in task '{task}': {error}")
    
    def log_search_query(self, tool_name: str, query: str):
        """Log search queries"""
        self.debug(f"Search tool '{tool_name}' executing query: {query}")
    
    def log_search_results(self, tool_name: str, query: str, result_count: int):
        """Log search results"""
        self.debug(f"Search tool '{tool_name}' returned {result_count} results for query: {query}")
    
    def log_user_input(self, cv_length: int, jd_length: int):
        """Log user input statistics"""
        self.info(f"User input received - CV length: {cv_length} chars, JD length: {jd_length} chars")
    
    def log_crew_execution(self, task_count: int, total_duration: float):
        """Log crew execution summary"""
        self.info(f"Crew execution completed - {task_count} tasks in {total_duration:.2f}s")

# Global logger instance
app_logger = Logger()

# Convenience functions
def log_info(message: str, extra: Optional[dict] = None):
    app_logger.info(message, extra)

def log_debug(message: str, extra: Optional[dict] = None):
    app_logger.debug(message, extra)

def log_warning(message: str, extra: Optional[dict] = None):
    app_logger.warning(message, extra)

def log_error(message: str, extra: Optional[dict] = None):
    app_logger.error(message, extra)

def log_critical(message: str, extra: Optional[dict] = None):
    app_logger.critical(message, extra)
