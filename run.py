#!/usr/bin/env python3
"""
MirrorMe - AI Personality Cloning System
Launch script for the Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import openai
        import langchain
        import faiss
        import plotly
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and add your OpenAI API key")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=' not in content or 'your-openai-api-key-here' in content:
            print("❌ OpenAI API key not configured in .env file!")
            print("Please add your OpenAI API key to the .env file")
            return False
    
    print("✅ Environment configuration looks good!")
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', '.streamlit', 'assets']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created!")

def main():
    """Main launcher function"""
    print("🪞 MirrorMe - AI Personality Cloning System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Launch Streamlit
    print("\n🚀 Launching MirrorMe...")
    print("🌐 Open your browser to: http://localhost:8501")
    print("📝 Start chatting to train your AI personality clone!")
    print("\n" + "=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using MirrorMe!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()