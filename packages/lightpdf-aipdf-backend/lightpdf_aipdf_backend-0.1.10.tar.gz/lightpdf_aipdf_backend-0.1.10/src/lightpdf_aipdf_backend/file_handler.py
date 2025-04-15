import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from pathlib import Path

from .config import UPLOADS_DIR
from .models import FileInfo
from .state import store_file_info, get_session_files

async def handle_file_upload(file: UploadFile, session_id: str) -> FileInfo:
    """处理文件上传请求
    
    Args:
        file: 上传的文件
        session_id: 会话ID
        
    Returns:
        FileInfo: 文件信息对象
        
    Raises:
        HTTPException: 文件上传失败时抛出
    """
    # 生成唯一文件名
    file_id = str(uuid4())
    filename = file.filename or "unknown_file"
    content_type = file.content_type or "application/octet-stream"
    
    # 确保文件名安全
    safe_filename = f"{file_id}_{filename}"
    file_path = UPLOADS_DIR / safe_filename
    
    # 确保UPLOADS_DIR存在
    UPLOADS_DIR.mkdir(exist_ok=True)
    
    # 保存文件
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 使用相对路径(仅文件名)
        relative_path = safe_filename
        
        # 创建文件信息
        file_info = FileInfo(
            file_id=file_id,
            filename=filename,
            content_type=content_type,
            path=relative_path
        )
        
        # 存储文件信息到会话
        store_file_info(session_id, file_info)
        
        return file_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

def get_file_references(file_ids: list[str], session_id: str) -> list[str]:
    """获取文件引用链接
    
    Args:
        file_ids: 文件ID列表
        session_id: 会话ID
        
    Returns:
        list[str]: 文件引用链接列表
    """
    file_urls = []
    session_files = get_session_files(session_id)
    
    for file_id in file_ids:
        if file_id in session_files:
            file_info = session_files[file_id]
            # 检查文件是否存在
            file_path = os.path.join(UPLOADS_DIR, file_info.path) if not os.path.isabs(file_info.path) else file_info.path
            if os.path.exists(file_path):
                # 根据文件类型添加不同的引用格式
                if file_info.content_type.startswith("image/"):
                    file_urls.append(f"![图片: {file_info.filename}]({file_info.path})")
                else:
                    file_urls.append(f"[文件: {file_info.filename}]({file_info.path})")
    
    return file_urls 