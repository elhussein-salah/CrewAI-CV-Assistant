import os
from dotenv import load_dotenv
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from config.ollama_config import OllamaConfig

load_dotenv()

class CrewConfig:
    """Configuration for CrewAI setup"""
    
    # Application settings
    APP_TITLE = os.getenv("APP_TITLE", "CrewAI CV Assistant")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Search API settings
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    
    @classmethod
    def get_llm(cls):
        """Initialize and return Ollama LLM instance"""
        try:
            llm_params = OllamaConfig.get_llm_params()
            llm = OllamaLLM(**llm_params)
            return llm
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")
    
    @classmethod
    def get_search_api_key(cls):
        """Get search API key if available"""
        return cls.SERPAPI_API_KEY if cls.SERPAPI_API_KEY else None
