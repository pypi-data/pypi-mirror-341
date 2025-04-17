# -*- coding:utf-8 -*-
# @Function  : llm_util
# @Author    : wjh
# @Time      : 2025-04-14
# Version    : 1.0
import json

from openai import OpenAI

from woodwtoolkit.common.func import print_line
from woodwtoolkit.conf import getenv


class LLMService:

    client: OpenAI = None

    def __init__(self, **kwargs):
        super().__init__()
        self.client = self.create_openai_client(**kwargs)

    def create_openai_client(self, api_key: str = None, base_url: str = None, **kwargs) -> OpenAI:
        """
        创建OpenRouter客户端
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: OpenRouter API的基础URL
        Returns:
            OpenAI: OpenRouter客户端实例
        """

        if api_key is None:
            api_key = getenv("OPENROUTER_API_KEY")

        if base_url is None:
            base_url = getenv("OPENROUTER_BASE_URL")

        kwargs.update({
            "api_key": api_key,
            "base_url": base_url,
        })

        self.client = OpenAI(**kwargs)
        return self.client

    def chat(self, message: str, **kwargs):
        try:
            model = kwargs.get('model', "google/gemini-2.0-flash-001")

            kwargs.update({
                "model": model,
                "messages": [{"role": "user", "content": message}],
                # "temperature": temperature
            })

            response = self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            # print(message.content)

            return { 'code':0 , 'content': message.content}

        except Exception as e:
            # print(e)
            return { 'code':1 , 'content': str(e)}

    def chat_with_history(self, messages: list, **kwargs):
        model = kwargs.get('model', "google/gemini-2.0-flash-001")

        kwargs.update({
            "model": model,
            "messages": messages,
            # "temperature": temperature
        })

        response = self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        messages.append(message)

        print_line('-')
        print(message.content)

        return messages

    def chat_with_tools(self, messages: list, tools: list, TOOL_MAPPING: dict, config: dict = None, **kwargs):
        if config is None:
            config = {}

        model = kwargs.get('model', "google/gemini-2.0-flash-001")
        openai_client = self.client

        kwargs.update({
            "model": model,
            "tools": tools,
            "messages": messages,
            # "temperature": temperature
        })

        no = 0
        while True:
            response = openai_client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            messages.append(message)
            no += 1

            print_line('-')
            print(f"第{no}次请求")
            print(message.content)

            if message.tool_calls is None:
                break

            # Now we process the requested tool calls, and use our book lookup tool
            for index, tool_call in enumerate(message.tool_calls, 1):
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                tool_response = TOOL_MAPPING[tool_name](**tool_args)
                content = json.dumps(tool_response)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": content,
                })

                print(f" + {index}.工具调用: {tool_name}")
                print(f" +   调用参数: {tool_args}")
                print(f" +   调用结果: {content}")

        print_line('*')
        print(f"共{no}次请求")
        print(message.content)

        return messages
