import os
from dotenv import load_dotenv

# Load environment variables - force override existing system vars
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    print(f"[CONFIG] Loading .env from: {dotenv_path}")
    load_dotenv(dotenv_path, override=True)

class Settings:
    """Application settings"""
    
    def __init__(self):
        # API Configuration
        self.api_host = os.getenv("API_HOST", "http://localhost")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        
        # OpenAI-compatible API Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        self.openai_model = os.getenv("OPENAI_MODEL")

# Create settings instance
settings = Settings()
