

import openai
import os

# 将您的OpenAI API 密钥存储在环境变量中
openai.api_key = "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"

# 指定模型和模型引擎ID
model_engine = "text-davinci-003"
model_prompt = {
    "model": model_engine,
    "temperature": 0.7,
    "max_tokens": 1024
}

# 初始化对话历史记录
conversation_history = ""

while True:
    # 接收用户输入
    prompt = input("You: ")

    # 将用户输入和对话历史记录添加到模型提示中
    model_prompt["prompt"] = conversation_history + prompt

    # 调用OpenAI的API并获取生成的文本
    response = openai.Completion.create(**model_prompt)
    output_text = response.choices[0].text.strip()

    # 将生成的文本添加到对话历史记录中
    conversation_history += prompt + "\n" + output_text + "\n"

    # 输出生成的文本
    print("AI: " + output_text)
