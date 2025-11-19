
import json,socket, threading
from openai import OpenAI

# 初始化 Kimi 客户端（复用原配置：moonshot 平台 API）
KIMI_API_KEY = "sk-0GWM8V9S2oYohUqBZe45lwlWdRyRscuJCEk7BkayEb872qy1"
client = OpenAI(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",  # Kimi 专属 base_url
)
def generate_kimi_stream(prompt, history_messages=None):
    """
    调用 Kimi 流式接口，返回 SSE 格式响应
    :param prompt: 当前用户输入
    :param history_messages: 对话历史（支持多轮对话）
    :return: 流式响应迭代器
    """
    # 初始化对话历史（包含系统提示）
    messages = [{"role": "system", "content": "你是Kimi AI助手，提供中文对话服务。"}]
    if history_messages:
        messages.extend(history_messages)
    # 添加当前用户输入
    messages.append({"role": "user", "content": prompt})

    try:
        # 调用 Kimi 模型（流式输出）
        response = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=messages,
            temperature=0.6,
            stream=True
        )

        # 迭代流式数据，封装为 SSE 格式
        for chunk in response:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                yield f"data: {json.dumps({'content': chunk_content})}\n\n"
        
        # 输出结束标记
        yield f"data: {json.dumps({'end': True})}\n\n"

    except Exception as e:
        # 错误信息流式返回
        yield f"data: {json.dumps({'error': f'调用失败：{str(e)}'})}\n\n"
