#!/usr/bin/env python3
"""
Setup script for MirrorMe - AI Personality Cloning System
"""

import os
import subprocess
import sys

def main():
    print("🪞 MirrorMe Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Consider using a virtual environment")
    
    # Check OpenAI API key
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'your-openai-api-key-here' in content:
                print("❌ Please set your OpenAI API key in .env file")
                print("   1. Get your API key from: https://platform.openai.com/account/api-keys")
                print("   2. Edit .env file and replace 'your-openai-api-key-here' with your actual key")
                print("   3. Run this setup script again")
                sys.exit(1)
            else:
                print("✅ OpenAI API key configured")
    else:
        print("❌ .env file not found")
        sys.exit(1)
    
    # Download NLTK data
    print("\n📥 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  NLTK download failed: {e}")
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    print("✅ Data directory created")
    
    print("\n🚀 Setup complete!")
    print("Run: streamlit run app.py")
    print("Or: python3 run.py")

if __name__ == "__main__":
    main()