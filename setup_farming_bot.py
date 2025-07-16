#!/usr/bin/env python3
"""
Setup Script for Macadamia Farming Bot
======================================

This script sets up the environment and trains the initial models
for the macadamia farming chatbot.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required Python packages"""
    logger.info("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "macadamia_bot/models/saved",
        "logs",
        "data/exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created directory: {directory}")

def check_environment_file():
    """Check if .env file exists and guide user"""
    if not os.path.exists('.env'):
        logger.warning("⚠️  .env file not found")
        logger.info("📝 Please copy .env.example to .env and add your Together AI API key")
        logger.info("   You can get an API key from: https://api.together.xyz/")
        
        # Create a basic .env file
        with open('.env', 'w') as f:
            f.write("# Add your Together AI API key here\n")
            f.write("TOGETHER_API_KEY=your_api_key_here\n")
        
        logger.info("✅ Created basic .env file - please edit it with your API key")
        return False
    else:
        logger.info("✅ .env file found")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    logger.info("Testing imports...")
    
    required_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'plotly',
        'requests',
        'yaml'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✅ {module}")
        except ImportError:
            logger.error(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        logger.error(f"Failed to import: {', '.join(failed_imports)}")
        return False
    
    logger.info("✅ All required modules imported successfully")
    return True

def train_initial_models():
    """Train the initial ML models"""
    logger.info("Training initial ML models...")
    
    try:
        from macadamia_bot.models.model_trainer import MacadamiaModelTrainer
        
        trainer = MacadamiaModelTrainer()
        results = trainer.train_all_models()
        
        logger.info("✅ Models trained successfully!")
        
        # Display results
        for model_name, metrics in results.items():
            if 'test_accuracy' in metrics:
                logger.info(f"   {model_name}: {metrics['test_accuracy']:.3f} accuracy")
            elif 'test_r2' in metrics:
                logger.info(f"   {model_name}: {metrics['test_r2']:.3f} R²")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Model training failed: {e}")
        logger.info("   Models will use fallback predictions until training succeeds")
        return False

def test_chatbot():
    """Test basic chatbot functionality"""
    logger.info("Testing chatbot functionality...")
    
    try:
        from macadamia_bot.core.chatbot import MacadamiaBot
        
        # Test without API key first
        bot = MacadamiaBot()
        
        # Test basic query
        response = bot.chat("Hello, I need help with macadamia farming")
        
        if response and 'final_response' in response:
            logger.info("✅ Chatbot basic functionality working")
            return True
        else:
            logger.warning("⚠️  Chatbot responded but format may be incorrect")
            return False
            
    except Exception as e:
        logger.error(f"❌ Chatbot test failed: {e}")
        return False

def create_demo_script():
    """Create a demo script for testing"""
    demo_content = '''#!/usr/bin/env python3
"""
Demo script for Macadamia Farming Bot
"""

from macadamia_bot.core.chatbot import MacadamiaBot

def main():
    print("🥜 Macadamia Farming Bot Demo")
    print("=" * 40)
    
    # Initialize bot
    bot = MacadamiaBot()
    
    # Sample farm data
    farm_data = {
        'soil_ph': 6.2,
        'temperature': 24,
        'humidity': 65,
        'rainfall': 120,
        'season': 'spring',
        'tree_age': 5
    }
    
    # Test queries
    test_queries = [
        "What should I do for pest management?",
        "When should I fertilize my trees?",
        "How do I know when to harvest?",
        "I want to get organic certification"
    ]
    
    for query in test_queries:
        print(f"\\n🧑‍🌾 Question: {query}")
        response = bot.chat(query, farm_data=farm_data)
        print(f"🤖 Response: {response['final_response'][:200]}...")
        print("-" * 40)

if __name__ == "__main__":
    main()
'''
    
    with open('demo_farming_bot.py', 'w') as f:
        f.write(demo_content)
    
    logger.info("✅ Created demo script: demo_farming_bot.py")

def main():
    """Main setup function"""
    print("🥜 Macadamia Farming Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        logger.error("Setup failed at dependency installation")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        logger.error("Setup failed at import testing")
        sys.exit(1)
    
    # Check environment file
    env_ok = check_environment_file()
    
    # Train models
    models_ok = train_initial_models()
    
    # Test chatbot
    chatbot_ok = test_chatbot()
    
    # Create demo script
    create_demo_script()
    
    # Final summary
    print("\\n" + "=" * 50)
    print("🎯 Setup Summary:")
    print("=" * 50)
    
    print(f"✅ Python version: OK")
    print(f"✅ Dependencies: OK")
    print(f"✅ Directories: OK")
    print(f"{'✅' if env_ok else '⚠️ '} Environment file: {'OK' if env_ok else 'Needs API key'}")
    print(f"{'✅' if models_ok else '⚠️ '} ML Models: {'OK' if models_ok else 'Using fallbacks'}")
    print(f"{'✅' if chatbot_ok else '⚠️ '} Chatbot: {'OK' if chatbot_ok else 'Basic functionality'}")
    
    print("\\n🚀 Next Steps:")
    if not env_ok:
        print("1. Add your Together AI API key to .env file")
    print("2. Run: streamlit run macadamia_farming_bot.py")
    print("3. Or test with: python demo_farming_bot.py")
    
    print("\\n📚 Documentation:")
    print("- README_FARMING.md: Comprehensive guide")
    print("- config/farming_config.yaml: Configuration options")
    print("- macadamia_bot/: Source code modules")
    
    if env_ok and models_ok and chatbot_ok:
        print("\\n🎉 Setup completed successfully! Your farming bot is ready to use.")
    else:
        print("\\n⚠️  Setup completed with warnings. Check the issues above.")

if __name__ == "__main__":
    main()

