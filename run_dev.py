#!/usr/bin/env python
"""
Development server runner for EduCrowd.
This script helps you run the Django development server with proper setup.
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_virtual_environment():
    """Check if we're in a virtual environment."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  No virtual environment detected. It's recommended to use one.")
        return False

def install_requirements():
    """Install Python requirements."""
    print("📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def setup_environment():
    """Set up environment variables."""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        env_example = Path('.env.example')
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✅ .env file created")
        else:
            print("❌ .env.example file not found")
            sys.exit(1)
    else:
        print("✅ .env file already exists")

def run_migrations():
    """Run Django migrations."""
    print("📊 Running migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrations completed")
    except subprocess.CalledProcessError:
        print("❌ Migration failed")
        sys.exit(1)

def create_superuser():
    """Create superuser if it doesn't exist."""
    print("👤 Checking for superuser...")
    try:
        # Check if superuser exists
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            'from django.contrib.auth import get_user_model; User = get_user_model(); print("exists" if User.objects.filter(is_superuser=True).exists() else "not_exists")'
        ], capture_output=True, text=True)
        
        if "not_exists" in result.stdout:
            print("👤 Creating superuser...")
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
            print("✅ Superuser created")
        else:
            print("✅ Superuser already exists")
    except subprocess.CalledProcessError:
        print("❌ Failed to create superuser")

def run_server():
    """Run Django development server."""
    print("🚀 Starting Django development server...")
    print("🌐 Access the application at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError:
        print("❌ Server failed to start")

def main():
    """Main function."""
    print("🚀 EduCrowd Development Server Setup")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    check_virtual_environment()
    
    # Setup
    setup_environment()
    install_requirements()
    run_migrations()
    create_superuser()
    
    print("\n" + "=" * 50)
    print("✅ Setup complete! Starting development server...")
    print("=" * 50)
    
    # Start server
    run_server()

if __name__ == '__main__':
    main()
