from openai import OpenAI
import json

def request_ai(message: str, api_key: str, prompt: str, mode = "chat") -> str:
    print(f"请求 AI，消息内容: {message}")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",)
    response = client.chat.completions.create(
        model="deepseek-chat" if mode == "chat" else "deepseek-reasoner",
        messages=[
            {"role": "system", "content": "你是一个遵守规则的游戏npc，你需要扮演用户要求的角色完成任务"},
            {"role": "user", "content": prompt + message}
        ],
        stream=False,
        temperature=1,
    )
    return response.choices[0].message.content # type: ignore 

def process(ai_reply: str, traits: list):
    reply_json = json.loads(ai_reply)
    active_traits = reply_json.get("active_traits", [])
    all_traits = reply_json.get("all_traits", [])

    new_all_traits = traits
    new_active_traits = []
    for i in active_traits:
        if i in all_traits:
            new_active_traits.append(i)
        if i not in all_traits:
            print(i)

    reply_json.update({"active_traits": new_active_traits})
    reply_json.update({"all_traits": new_all_traits})
    return reply_json