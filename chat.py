from openai import OpenAI

def request_ai(message: str, user_prompt: str, api_key: str, prompt: str) -> str:
    print(f"请求 AI，消息内容: {message}，用户提示词: {user_prompt}")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt + user_prompt + message}
        ],
        stream=False,
        temperature=1
    )
    return response.choices[0].message.content # type: ignore 