from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import openai
import os

# 将您的OpenAI API 密钥存储在环境变量中
openai.api_key = "your openai api key"

# 初始化Flask应用程序和SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# 指定模型和模型引擎ID
model_engine = "text-davinci-003"
model_prompt = {
    "model": model_engine,
    "temperature": 0.7,
    "max_tokens": 1024
}

# 初始化对话历史记录
conversation_history = ""

# 处理"/"路由
@app.route('/')
def index():
    return render_template('index.html')

# 处理"message"事件
@socketio.on('message')
def handle_message(message):
    global conversation_history
    prompt = message['data']
    # 将用户输入和对话历史记录添加到模型提示中
    model_prompt["prompt"] = conversation_history + prompt
    print("you:"+ prompt)
    # 调用OpenAI的API并获取生成的文本
    response = openai.Completion.create(**model_prompt)
    output_text = response.choices[0].text.strip()
    print("ai:"+output_text)
    # 将生成的文本添加到对话历史记录中
    conversation_history += prompt + "\n" + output_text + "\n"
    # 发送"message"事件，将生成的文本发送给客户端
    emit('message', {'data': output_text})

if __name__ == '__main__':
    socketio.run(app)
