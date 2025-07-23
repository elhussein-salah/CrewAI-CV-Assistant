import os
from dotenv import load_dotenv

load_dotenv()

class OllamaConfig:
    """Configuration for Ollama LLM"""
    
    MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    TEMPERATURE = 0.7
    TOP_P = 0.9
    
    # Model-specific configurations
    MODEL_CONFIGS = {
        "llama3": {
            "max_tokens": 4096,
            "context_window": 8192
        },
        "mistral": {
            "max_tokens": 4096,
            "context_window": 8192
        },
        "codellama": {
            "max_tokens": 4096,
            "context_window": 16384
        }
    }
    
    @classmethod
    def get_model_config(cls):
        """Get configuration for the current model"""
        return cls.MODEL_CONFIGS.get(cls.MODEL, cls.MODEL_CONFIGS["llama3"])
    
    @classmethod
    def get_llm_params(cls):
        """Get LLM parameters for initialization"""
        config = cls.get_model_config()
        return {
            "model": cls.MODEL,
            "base_url": cls.BASE_URL,
            "temperature": cls.TEMPERATURE,
            "top_p": cls.TOP_P,
            "num_predict": config["max_tokens"]
        }
