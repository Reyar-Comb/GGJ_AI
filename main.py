from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from chat import request_ai, process
import json
import random


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") 
role_prompt: str = os.getenv("ROLE_PROMPT")  # type: ignore
story_prompt: str = os.getenv("STORY_PROMPT")  # type: ignore
chatrule_prompt: str = os.getenv("CHATRULE_PROMPT")  # type: ignore

profile_str = open("resources/profile.json", "r", encoding="utf-8").read()
profile_json = json.loads(profile_str)


if role_prompt:
    print(f"成功加载系统提示词, 提示词前50个字符: {role_prompt[:50]}...")
else:
    print("错误：未能读取到 ROLE_PROMPT，请检查 .env 文件路径和格式")

app = Flask(__name__)
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "status": "success",
        "message": "API is working"
    })
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
    print(ai_reply)
    process(ai_reply, traits)

    return jsonify({
        "status": "success",
        "player_ip": player_ip,
        "reply": ai_reply
    })

@app.route('/api/story', methods=['POST'])
def story():
    data = request.json
    player_ip = request.remote_addr
    age_group = data.get('age_group')
    sex = data.get('sex')
    print(f"收到玩家 [{player_ip}] 的消息: 年龄段: {age_group}, 性别: {sex}")

    matches = [p for p in profile_json if p["age_group"] == int(age_group) and p["sex"] == sex]  # type: ignore
    if matches:
        story_text = random.choice(matches)["story"]  # type: ignore
    else:
        story_text = "我是伪人"

    return jsonify({
        "status": "success",
        "player_ip": player_ip,
        "reply": f"{{\"story\": \"{story_text}\"}}"
    })

def main():
    print("Hello from ggj-ai!")
    app.run(host='0.0.0.0', port=8000, debug=True)
if __name__ == "__main__":
    main()
