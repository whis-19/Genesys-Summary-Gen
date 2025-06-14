#!/usr/bin/env python
# filepath: d:\Abdullah\GENESYS RAG\run_app.py
"""
Launcher script for the Document Summarization App
"""
import os
import subprocess
import sys

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import PyPDF2
        from dotenv import load_dotenv
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except Exception as e:
            print(f"Failed to install requirements: {e}")
            return False

def main():
    """Launch the Streamlit app"""
    if not check_requirements():
        print("Error: Could not install required dependencies.")
        return
    
    print("Starting Document Summarization App...")
    print("Loading interface in your browser...")
    
    # Run the Streamlit app
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()
