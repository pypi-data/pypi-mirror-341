import json
from typing import Dict, List, AsyncGenerator, Any

def validate_and_fix_messages(messages: List[Dict]) -> List[Dict]:
    """验证并修复消息格式，确保工具调用和响应的匹配
    
    Args:
        messages: 消息列表
        
    Returns:
        List[Dict]: 修复后的消息列表
    """
    if not messages:
        return []
    
    fixed_messages = []
    tool_call_ids = {}  # 用于跟踪工具调用ID及其对应的工具名称
    
    for msg in messages:
        # 检查assistant角色的工具调用
        if msg["role"] == "assistant" and "tool_calls" in msg:
            # 存储工具调用ID和对应的工具名称
            for tool_call in msg["tool_calls"]:
                tool_call_ids[tool_call["id"]] = tool_call["function"]["name"]
        
        # 处理tool角色的响应，确保有对应的tool_call_id和name
        if msg["role"] == "tool":
            if "tool_call_id" not in msg or not msg["tool_call_id"]:
                continue
                
            if "name" not in msg or not msg["name"]:
                # 如果能找到对应的工具调用，自动填充name
                if msg["tool_call_id"] in tool_call_ids:
                    msg["name"] = tool_call_ids[msg["tool_call_id"]]
                else:
                    continue
        
        fixed_messages.append(msg)
    
    return fixed_messages

async def async_generator_to_json_stream(generator: AsyncGenerator) -> AsyncGenerator:
    """将异步生成器转换为JSON流
    
    Args:
        generator: 异步生成器
        
    Yields:
        bytes: JSON流
    """
    async for item in generator:
        yield json.dumps(item, ensure_ascii=False).encode('utf-8') + b'\n' 