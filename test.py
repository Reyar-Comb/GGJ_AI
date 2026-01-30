import asyncio
import httpx

async def test(client: httpx.AsyncClient, message: str, target: list[str], mask: list[str], mode: str) -> str:
    """
    使用异步客户端发送请求
    """
    data = {
        "content": message,
        "prompt": f"Target: {target}, Mask: {mask}, Mode: {mode}",
        "player_id": "test_player"
    }
    print(f"请求数据: {data}")
    try:
        # 发送异步 POST 请求
        response = await client.post("http://localhost:8000/api/chat", json=data, timeout=60.0)
        
        # 检查是否报错 (防止之前的 JSONDecodeError)
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"
            
        return response.json().get("reply", "无恢复")
    except Exception as e:
        return f"请求异常: {str(e)}"

async def async_test(message: str, target: list[str], mask: list[str], mode: str  ) -> str:
    async with httpx.AsyncClient() as client:
        task = test(client, message, target, mask, mode)
        
        # 3. 等待所有任务完成
        replies = await asyncio.gather(task)
        return f"结果: {replies[0]}"
if __name__ == "__main__":
    # 4. 重要：使用 asyncio.run 启动异步主入口
    while(True):
        input_message = input("请输入测试消息 (或输入 'exit' 退出): ")
        if input_message.lower() == 'exit':
            break
        result = asyncio.run(async_test(message=input_message, target=["L1", "L2", "L3"], mask=["L1", "L3", "L4"], mode="Intersection"))
        print(result)   