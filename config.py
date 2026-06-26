"""
Configuration settings for the hiring agent application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Global development mode flag
DEVELOPMENT_MODE = True
LLAMACPP_ENDPOINT = os.getenv("LLAMACPP_ENDPOINT","")