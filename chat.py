from openai import OpenAI

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