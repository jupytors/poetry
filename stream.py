import json
import requests

# Deepseek-Ollama 核心配置（本地服务）
OLLAMA_URL = "http://localhost:8434/api/generate"
DEFAULT_MODEL = "deepseek-r1:7b"  # 已安装的 deepseek 模型名

def generate_deepseek_stream1(prompt, history_messages=None):
    """
    调用本地 Deepseek-Ollama 流式接口，返回 SSE 格式响应
    :param prompt: 当前用户输入
    :param history_messages: 对话历史（格式：[{"role": "user/assistant", "content": "..."}]）
    :return: 流式响应迭代器（SSE 格式）
    """
    # 构建对话历史（系统提示+历史消息+当前输入）
    messages = [{"role": "system", "content": "你是Deepseek AI助手，提供中文对话服务。"}]
    if history_messages:
        # 转换对话历史为 Ollama 支持的 prompt 格式（user: ...\nassistant: ...）
        for msg in history_messages:
            role = "用户" if msg["role"] == "user" else "助手"
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    # 拼接完整 prompt（Ollama 不直接支持 messages 字段，需手动拼接）
    full_prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            full_prompt += f"系统提示：{msg['content']}\n"
        elif msg["role"] == "user":
            full_prompt += f"用户：{msg['content']}\n"
        elif msg["role"] == "assistant":
            full_prompt += f"助手：{msg['content']}\n"
    full_prompt += "助手："  # 触发模型继续回答

    # 发起 Ollama 流式请求
    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": DEFAULT_MODEL,
                "prompt": full_prompt,
                "stream": True,
                "timeout": 300,
                "options": {"temperature": 0.6}  # 温度参数
            },
            stream=True
        )
        response.raise_for_status()  # 触发 4xx/5xx 错误

        # 流式迭代响应，封装为 SSE 格式
        for line in response.iter_lines(chunk_size=1024):
            if line:
                try:
                    data = json.loads(line.decode("utf-8").strip())
                    if "response" in data:
                        yield f"data: {json.dumps({'content': data['response']})}\n\n"
                    # 检测对话结束
                    if data.get("done", False):
                        yield f"data: {json.dumps({'end': True})}\n\n"
                        break
                except json.JSONDecodeError:
                    continue

    except requests.exceptions.RequestException as e:
        error_msg = f"调用失败：{str(e)}"
        if "Connection refused" in error_msg:
            error_msg += "（请先启动 Ollama 服务：ollama serve）"
        yield f"data: {json.dumps({'error': error_msg})}\n\n"


def generate_deepseek_stream(prompt, history_messages=None):
    """
    调用本地 Deepseek-Ollama 流式接口，返回 SSE 格式响应
    :param prompt: 当前用户输入
    :param history_messages: 对话历史（格式：[{"role": "user/assistant", "content": "..."}]）
    :return: 流式响应迭代器（SSE 格式）
    """
    # 构建对话历史（系统提示+历史消息+当前输入）
    messages = [{"role": "system", "content": "你是Deepseek AI助手，提供中文对话服务。"}]
    if history_messages:
        for msg in history_messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    # 拼接完整 prompt
    full_prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            full_prompt += f"系统提示：{msg['content']}\n"
        elif msg["role"] == "user":
            full_prompt += f"用户：{msg['content']}\n"
        elif msg["role"] == "assistant":
            full_prompt += f"助手：{msg['content']}\n"
    
    full_prompt += "助手："  # 触发模型继续回答

    # 发起 Ollama 流式请求
    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": DEFAULT_MODEL,
                "prompt": full_prompt,
                "stream": True,
                "timeout": 300,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 4000
                }
            },
            stream=True
        )
        response.raise_for_status()

        # 流式迭代响应，封装为 SSE 格式
        for line in response.iter_lines(chunk_size=1024):
            if line:
                try:
                    data = json.loads(line.decode("utf-8").strip())
                    if "response" in data:
                        yield f"data: {json.dumps({'content': data['response']})}\n\n"
                    if "thoughts" in data:
                        yield f"data: {json.dumps({'thoughts': data['thoughts']})}\n\n"
                    if data.get("done", False):
                        yield f"data: {json.dumps({'end': True})}\n\n"
                        break
                except json.JSONDecodeError:
                    continue

    except requests.exceptions.RequestException as e:
        error_msg = f"调用失败：{str(e)}"
        if "Connection refused" in error_msg:
            error_msg += "（请先启动 Ollama 服务：ollama serve）"
        yield f"data: {json.dumps({'error': error_msg})}\n\n"
