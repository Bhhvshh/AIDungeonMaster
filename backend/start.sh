#!/bin/bash

# AI Dungeon Master Backend Startup Script
# This script installs dependencies and starts the backend server

set -e

echo "🧙 AI Dungeon Master - Backend Startup"
echo "======================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please configure .env file with your GEMINI_API_KEY"
    echo "   Edit: backend/.env"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Display API info
echo ""
echo "✅ Backend is ready!"
echo "🚀 Starting server..."
echo ""
echo "📍 API Base: http://localhost:5000"
echo "📖 API Docs: http://localhost:5000/docs"
echo ""

# Start the server
python main.py
