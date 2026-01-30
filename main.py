from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    player_content = data.get('content')
    player_id = data.get('player_id')
    print(f"收到玩家 [{player_id}] 的消息: {player_content}")

    ai_reply = "fku"

    return jsonify({
        "status": "success",
        "player_id": player_id,
        "reply": ai_reply
    })

def main():
    print("Hello from ggj-ai!")
if __name__ == "__main__":
    main()
