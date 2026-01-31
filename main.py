from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from chat import request_ai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") 
role_prompt: str = os.getenv("ROLE_PROMPT")  # type: ignore
story_prompt: str = os.getenv("STORY_PROMPT")  # type: ignore
chatrule_prompt: str = os.getenv("CHATRULE_PROMPT")  # type: ignore


if role_prompt:
    print(f"成功加载系统提示词, 提示词前50个字符: {role_prompt[:50]}...")
else:
    print("错误：未能读取到 ROLE_PROMPT，请检查 .env 文件路径和格式")

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    player_ip = request.remote_addr
    player_content = data.get('content', "")
    traits = data.get('traits', list())
    background = f"年龄{data.get('age', "")}, 性别{data.get('sex', '')}, 背景故事{data.get('story', '')}"
    patience = data.get('patience')
    print(f"收到玩家 [{player_ip}] 的消息: {player_content}, 特质: {traits}, 背景: {background}")

    prompt = f"{role_prompt} \n {chatrule_prompt} \n 玩家输入问题：{player_content} \n 你应当表现出的特质集合：{traits} \n 你的背景信息：{background} \n 你的耐心值为：{patience}。请根据耐心值调整你的回复长度和详细程度。"
    ai_reply = request_ai(
        message=player_content, 
        api_key=api_key, #type: ignore
        prompt=prompt
    )

    return jsonify({
        "status": "success",
        "player_ip": player_ip,
        "reply": ai_reply
    })

@app.route('/api/story', methods=['POST'])
def story():
    data = request.json
    player_ip = request.remote_addr
    age = data.get('age')
    sex = data.get('sex')
    traits = data.get('Traits', list())
    print(f"收到故事请求: 年龄: {age}, 性别: {sex}, 特质: {traits}")
    prompt = f"{role_prompt} \n {story_prompt} \n 年龄: {age}, 性别: {sex}, 特质: {traits}"
    ai_reply = request_ai(
        message="",
        api_key=api_key,  # type: ignore
        prompt=prompt
    )
    return jsonify({
        "status": "success",
        "player_ip": player_ip,
        "reply": ai_reply
    })

def main():
    print("Hello from ggj-ai!")
    app.run(host='0.0.0.0', port=8000, debug=True)
if __name__ == "__main__":
    main()
