"""Setup script for CodeSwitch AI backend"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_venv():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠ Warning: Not running in a virtual environment")
        print("  Recommended: Create and activate a virtual environment")
        print("  Windows: python -m venv venv && venv\\Scripts\\activate")
        print("  Linux/Mac: python -m venv venv && source venv/bin/activate")
        return False
    print("✓ Running in virtual environment")
    return True

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("\n⚠ .env file not found")
            print("  Creating .env from .env.example...")
            env_file.write_text(env_example.read_text())
            print("✓ .env file created")
            print("  ⚠ Please edit .env and add your GEMINI_API_KEY")
            return False
        else:
            print("❌ Neither .env nor .env.example found")
            return False
    
    # Check if GEMINI_API_KEY is set
    env_content = env_file.read_text()
    if "your_gemini_api_key_here" in env_content or "GEMINI_API_KEY=" not in env_content:
        print("⚠ GEMINI_API_KEY not configured in .env")
        print("  Please edit .env and add your Gemini API key")
        return False
    
    print("✓ .env file configured")
    return True

def check_data_directory():
    """Check if data directory exists"""
    data_dir = Path("..") / "data"
    if not data_dir.exists():
        print(f"\n⚠ Data directory not found: {data_dir}")
        print("  Creating data directory...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print("✓ Data directory created")
        print("  Add markdown files to ../data/ for RAG ingestion")
        return False
    
    md_files = list(data_dir.glob("*.md"))
    if not md_files:
        print(f"\n⚠ No markdown files found in {data_dir}")
        print("  Add markdown files to ../data/ for RAG ingestion")
        return False
    
    print(f"✓ Data directory found with {len(md_files)} markdown files")
    return True

def main():
    """Run setup checks"""
    print("="*60)
    print("CodeSwitch AI - Backend Setup")
    print("="*60 + "\n")
    
    checks = []
    
    # Run checks
    checks.append(("Python version", check_python_version()))
    checks.append(("Virtual environment", check_venv()))
    checks.append(("Dependencies", install_dependencies()))
    checks.append(("Environment file", check_env_file()))
    checks.append(("Data directory", check_data_directory()))
    
    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    
    for name, status in checks:
        symbol = "✓" if status else "⚠"
        print(f"{symbol} {name}")
    
    all_passed = all(status for _, status in checks)
    
    if all_passed:
        print("\n✓ Setup complete! You can now run:")
        print("  python main.py")
    else:
        print("\n⚠ Setup incomplete. Please address the warnings above.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
