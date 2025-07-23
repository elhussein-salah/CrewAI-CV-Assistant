#!/usr/bin/env python3
"""
Test script for CrewAI CV Assistant components
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.crew_config import CrewConfig
        from config.ollama_config import OllamaConfig
        print("✅ Config modules imported")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from agents.cv_evaluator import CVEvaluatorAgent
        from agents.cv_improver import CVImproverAgent
        from agents.skill_recommender import SkillRecommenderAgent
        from agents.job_finder import JobFinderAgent
        print("✅ Agent modules imported")
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False
    
    try:
        from tools.search_tool import create_search_tools
        from utils.text_cleaner import TextCleaner
        from utils.pdf_reader import PDFReader
        from utils.logger import app_logger
        print("✅ Utility modules imported")
    except Exception as e:
        print(f"❌ Utility import failed: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🔗 Testing Ollama connection...")
    
    try:
        from config.crew_config import CrewConfig
        llm = CrewConfig.get_llm()
        
        start_time = time.time()
        response = llm.invoke("Hello! This is a test message. Please respond with 'Test successful'.")
        duration = time.time() - start_time
        
        print(f"✅ Ollama connection successful (Response time: {duration:.2f}s)")
        print(f"📝 Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_text_processing():
    """Test text processing utilities"""
    print("\n📝 Testing text processing...")
    
    try:
        from utils.text_cleaner import TextCleaner
        
        cleaner = TextCleaner()
        
        # Test CV cleaning
        sample_cv = "John   Doe\n\n\nSoftware   Engineer\n\nPython, JavaScript"
        cleaned_cv = cleaner.clean_cv_text(sample_cv)
        print(f"✅ CV cleaning: '{sample_cv}' -> '{cleaned_cv}'")
        
        # Test skill extraction
        skills = cleaner.extract_skills_from_text("I have experience with Python, React, and MySQL")
        print(f"✅ Skill extraction: {skills}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processing failed: {e}")
        return False

def test_search_tools():
    """Test search tool functionality"""
    print("\n🔍 Testing search tools...")
    
    try:
        from tools.search_tool import create_search_tools
        
        tools = create_search_tools()
        print(f"✅ Created {len(tools)} search tools")
        
        # Test basic search (with timeout)
        if tools:
            tool = tools[0]  # Job search tool
            print(f"✅ First tool: {tool.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Search tools failed: {e}")
        return False

def test_sample_data():
    """Test loading sample data"""
    print("\n📁 Testing sample data...")
    
    try:
        # Check if sample files exist
        sample_files = ['data/sample_cv.txt', 'data/sample_jd.txt']
        
        for file_path in sample_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✅ {file_path}: {len(content)} characters")
            else:
                print(f"❌ {file_path} not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from agents.cv_evaluator import CVEvaluatorAgent
        
        print("Initializing CV Evaluator agent...")
        agent = CVEvaluatorAgent()
        print("✅ CV Evaluator agent initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 CrewAI CV Assistant - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Ollama Connection", test_ollama_connection),
        ("Text Processing", test_text_processing),
        ("Search Tools", test_search_tools),
        ("Sample Data", test_sample_data),
        ("Agent Initialization", test_agent_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n{'=' * 20} {name} {'=' * 20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {name} test PASSED")
            else:
                print(f"❌ {name} test FAILED")
        except Exception as e:
            print(f"❌ {name} test ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main()
