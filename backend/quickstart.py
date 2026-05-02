#!/usr/bin/env python3
"""
Quick start script for AI Dungeon Master - Backend
Checks dependencies and starts the server
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_env_file():
    """Check and create .env file if needed"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        if os.path.exists(".env.example"):
            print("   Creating .env from template...")
            with open(".env.example", "r") as f:
                example = f.read()
            with open(".env", "w") as f:
                f.write(example)
            print("✅ Created .env file")
            print("   ⚠️  IMPORTANT: Update GEMINI_API_KEY in .env!")
        return False
    else:
        print("✅ .env file found")
        with open(".env", "r") as f:
            content = f.read()
            if "GEMINI_API_KEY=your_" in content:
                print("   ⚠️  IMPORTANT: Update GEMINI_API_KEY in .env!")
                return False
        return True

def check_venv():
    """Check if virtual environment exists"""
    venv_path = "venv"
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment found at {venv_path}/")
        return True
    else:
        print(f"⚠️  Virtual environment not found")
        print(f"   Creating {venv_path}...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"✅ Created {venv_path}/")
        return True

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ Required packages installed")
        return True
    except ImportError:
        print("⚠️  Some packages missing")
        print("   Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True

def main():
    """Main startup routine"""
    print("\n" + "="*50)
    print("🧙 AI Dungeon Master - Backend")
    print("="*50 + "\n")
    
    # Checks
    print("📋 Running checks...\n")
    check_python_version()
    check_venv()
    check_dependencies()
    env_ready = check_env_file()
    
    if not env_ready:
        print("\n⚠️  Please configure .env and run again")
        return
    
    print("\n" + "="*50)
    print("🚀 Starting Backend Server")
    print("="*50 + "\n")
    
    print("📍 API Base: http://localhost:5000")
    print("📖 API Docs: http://localhost:5000/docs")
    print("📊 Status:   http://localhost:5000/api/status")
    print("\n🔄 Starting uvicorn server...\n")
    
    # Start the server
    try:
        os.system("python main.py")
    except KeyboardInterrupt:
        print("\n\n👋 Backend shutdown gracefully")

if __name__ == "__main__":
    main()
