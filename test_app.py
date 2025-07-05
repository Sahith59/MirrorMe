#!/usr/bin/env python3
"""
Test script for MirrorMe components
"""

import os
import sys
from utils.mirror_agent import MirrorAgent
from utils.memory_manager import MemoryManager
from utils.personality_analyzer import PersonalityAnalyzer

def test_imports():
    """Test all imports"""
    print("🧪 Testing imports...")
    try:
        import streamlit
        import openai
        import langchain
        import faiss
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        from langchain_core.documents import Document
        from langchain_community.vectorstores import FAISS
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("🧪 Testing configuration...")
    try:
        from config import Config
        print(f"✅ Config loaded - Model: {Config.MODEL_NAME}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_memory_manager():
    """Test memory manager"""
    print("🧪 Testing memory manager...")
    try:
        memory = MemoryManager()
        memory.add_message("user", "Hello, this is a test message!")
        messages = memory.get_conversation_context(limit=1)
        print(f"✅ Memory manager working - {len(messages)} message(s) stored")
        return True
    except Exception as e:
        print(f"❌ Memory manager error: {e}")
        return False

def test_personality_analyzer():
    """Test personality analyzer"""
    print("🧪 Testing personality analyzer...")
    try:
        analyzer = PersonalityAnalyzer()
        test_messages = ["Hello there!", "How are you doing?", "I love programming!"]
        result = analyzer._calculate_message_statistics(test_messages)
        print(f"✅ Personality analyzer working - analyzed {len(test_messages)} messages")
        return True
    except Exception as e:
        print(f"❌ Personality analyzer error: {e}")
        return False

def test_mirror_agent():
    """Test mirror agent (without API call)"""
    print("🧪 Testing mirror agent initialization...")
    try:
        agent = MirrorAgent()
        progress = agent.get_learning_progress()
        print(f"✅ Mirror agent working - Stage: {progress['learning_stage']}")
        return True
    except Exception as e:
        print(f"❌ Mirror agent error: {e}")
        return False

def main():
    """Run all tests"""
    print("🪞 MirrorMe Component Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_memory_manager,
        test_personality_analyzer,
        test_mirror_agent
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! MirrorMe is ready to go!")
        print("\nTo start the application:")
        print("  python3 run.py")
        print("  or")
        print("  streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()