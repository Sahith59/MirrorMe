import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Memory settings
    MAX_MEMORY_ITEMS = 1000
    SIMILARITY_THRESHOLD = 0.7
    
    # Personality analysis settings
    PERSONALITY_ANALYSIS_FREQUENCY = 10  # Every 10 messages
    MIN_MESSAGES_FOR_ANALYSIS = 5
    
    # UI settings
    THEME_COLOR = "#6366f1"
    ACCENT_COLOR = "#8b5cf6"
    
    # Model settings
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    MAX_TOKENS = 150