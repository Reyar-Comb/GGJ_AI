from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from chat import request_ai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") 
prompt: str = os.getenv("AI_PROMPT")  # type: ignore


if prompt:
    print(f"成功加载系统提示词，长度: {len(prompt)}")
    print(f"提示词前50个字符: {prompt[:50]}...")
else:
    print("错误：未能读取到 AI_PROMPT，请检查 .env 文件路径和格式")



app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    player_content = data.get('content')
    player_id = data.get('player_id')
    player_prompt = data.get('prompt')
    print(f"收到玩家 [{player_id}] 的消息: {player_content}, 使用提示词: {player_prompt}")

    ai_reply = request_ai(
        message=player_content, 
        user_prompt=player_prompt, 
        api_key=api_key, #type: ignore
        prompt=prompt
    )

    return jsonify({
        "status": "success",
        "player_id": player_id,
        "reply": ai_reply
    })


def main():
    print("Hello from ggj-ai!")
    app.run(host='0.0.0.0', port=8000, debug=True)
if __name__ == "__main__":
    main()
