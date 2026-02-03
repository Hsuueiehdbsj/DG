import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # or "anthropic"
    
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_TEXT_FORMATS = [".txt", ".md", ".py", ".json", ".csv"]
    SUPPORTED_DOC_FORMATS = [".pdf", ".docx"]
    SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".webp"]