from typing import List, Optional, Dict
from pydantic import BaseModel

class FileInfo(BaseModel):
    """文件信息模型"""
    file_id: str
    filename: str
    content_type: str
    path: str

class Message(BaseModel):
    """聊天消息模型"""
    role: str
    content: str
    file_ids: Optional[List[str]] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    """聊天请求模型"""
    content: str
    file_ids: Optional[List[str]] = None 