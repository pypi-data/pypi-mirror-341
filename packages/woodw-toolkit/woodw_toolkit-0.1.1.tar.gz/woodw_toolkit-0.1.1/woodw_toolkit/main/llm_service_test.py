# -*- coding:utf-8 -*-
# @Function  : llm_service_test
# @Author    : wjh
# @Time      : 2025-04-14
# Version    : 1.0

from woodw_toolkit.services.llm_service import LLMService


def test_basic_chat():
    """测试基础对话功能"""
    llm_service = LLMService()
    
    # 基础对话测试
    messages = "你好，请介绍一下你自己"
    messages = llm_service.chat(messages)
    
    print("\n=== 基础对话测试结果 ===")
    print(messages)


def test_tool_chat():
    """测试工具对话功能"""
    llm_service = LLMService()
    
    # 定义工具
    tools = [{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如：北京"
                    }
                },
                "required": ["location"]
            }
        }
    }]

    # 工具实现
    def get_current_weather(location):
        return {
            "location": location,
            "temperature": "25°C",
            "condition": "晴天"
        }

    tool_mapping = {
        "get_current_weather": get_current_weather
    }

    # 工具对话测试
    messages = [{"role": "user", "content": "北京今天天气怎么样？"}]
    messages = llm_service.chat_with_tools(messages, tools, tool_mapping)
    
    print("\n=== 工具对话测试结果 ===")
    for msg in messages:
        if msg.get("role") == "tool":
            print(f"工具调用 - {msg['name']}: {msg['content']}")
        else:
            print(f"{msg['role']}: {msg['content']}")


if __name__ == '__main__':
    test_basic_chat()
    # test_tool_chat()