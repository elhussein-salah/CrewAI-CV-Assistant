# CrewAI CV Assistant Package
# A comprehensive AI-powered CV analysis and job matching system

__version__ = "1.0.0"
__author__ = "CrewAI CV Assistant Team"
__description__ = "AI-powered CV analysis system using CrewAI, Streamlit, and Ollama"

from config.crew_config import CrewConfig
from config.ollama_config import OllamaConfig

# Package level imports
from agents.cv_evaluator import CVEvaluatorAgent
from agents.cv_improver import CVImproverAgent  
from agents.skill_recommender import SkillRecommenderAgent
from agents.job_finder import JobFinderAgent

from tools.search_tool import SearchTool, create_search_tools
from utils.text_cleaner import TextCleaner
from utils.pdf_reader import PDFReader
from utils.logger import app_logger

__all__ = [
    'CrewConfig',
    'OllamaConfig', 
    'CVEvaluatorAgent',
    'CVImproverAgent',
    'SkillRecommenderAgent', 
    'JobFinderAgent',
    'SearchTool',
    'create_search_tools',
    'TextCleaner',
    'PDFReader',
    'app_logger'
]
