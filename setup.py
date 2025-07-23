#!/usr/bin/env python3
"""
Setup script for CrewAI CV Assistant
This script helps with initial setup and configuration
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        pass
    
    print("❌ Ollama is not running or not installed")
    print("Please install Ollama from: https://ollama.ai/")
    return False

def check_ollama_model():
    """Check if required model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            required_models = ['llama3', 'mistral', 'codellama']
            available_models = [model for model in required_models if any(model in name for name in model_names)]
            
            if available_models:
                print(f"✅ Available models: {available_models}")
                return True
            else:
                print("❌ No compatible models found")
                print("Please pull a model: ollama pull llama3")
                return False
    except:
        pass
    
    return False

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'data', 'temp']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Setup environment variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    print("✅ Environment file found")
    return True

def test_agents():
    """Test if agents can be initialized"""
    try:
        sys.path.append('.')
        from config.crew_config import CrewConfig
        
        # Test LLM connection
        llm = CrewConfig.get_llm()
        response = llm.invoke("Hello, this is a test.")
        
        print("✅ Agent initialization test passed")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 CrewAI CV Assistant Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Ollama Installation", check_ollama_installation),
        ("Ollama Model", check_ollama_model),
        ("Dependencies", install_dependencies),
        ("Directories", create_directories),
        ("Environment", setup_environment),
        ("Agent Test", test_agents)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if check_func():
            passed += 1
        else:
            print(f"❌ {name} check failed")
    
    print("\n" + "=" * 40)
    print(f"Setup Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Setup completed successfully!")
        print("\nTo start the application:")
        print("streamlit run app.py")
    else:
        print("⚠️ Some checks failed. Please resolve the issues above.")
        
    return passed == total

if __name__ == "__main__":
    main()
