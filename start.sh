#!/bin/bash

# JHRIS Quick Start Script
# This script helps you get started with JHRIS quickly

set -e

echo "=========================================="
echo "   JHRIS Quick Start Setup"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing backend dependencies..."
    npm install
else
    echo "✅ Backend dependencies already installed"
fi

# Create data directory
if [ ! -d "data" ]; then
    mkdir -p data
    echo "✅ Created data directory"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Using default configuration."
    echo "⚠️  IMPORTANT: Change JWT_SECRET in production!"
fi

echo ""
echo "Starting backend server..."
npm start &
BACKEND_PID=$!
echo "✅ Backend server started (PID: $BACKEND_PID)"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 5

# Check if backend is running
if curl -s http://localhost:3001/api/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:3001"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend/public

echo ""
echo "=========================================="
echo "   JHRIS is ready!"
echo "=========================================="
echo ""
echo "Backend API: http://localhost:3001"
echo "Frontend:    Open index.html in your browser"
echo ""
echo "Default admin credentials:"
echo "  Create an account, then manually set role to 'admin' in database"
echo ""
echo "To stop the backend server:"
echo "  kill $BACKEND_PID"
echo ""
echo "For production deployment, see docs/PRODUCTION.md"
echo ""
