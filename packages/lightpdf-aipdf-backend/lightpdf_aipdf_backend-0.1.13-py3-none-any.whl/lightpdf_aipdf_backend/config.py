import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 文件上传目录
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

class Config:
    """应用配置类"""
    MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
    BASE_URL = os.getenv("OPENAI_BASE_URL")
    API_KEY = os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def validate(cls):
        """验证关键配置项"""
        if not cls.API_KEY:
            raise ValueError("Missing OpenAI API Key") 