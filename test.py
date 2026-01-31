import asyncio
import httpx
import json
import random

Persona = {
    "P1": ['L1', 'L2', 'L3'], 
    "P2": ['L1', 'L2', 'L4'],
    "P3": ['L1', 'L3', 'L5'],
    "P4": ['L1', 'L4', 'L6'],
    "P5": ['L2', 'L5', 'L6'],
    "P6": ['L3', 'L4', 'L5'],
    "P7": ['L3', 'L4', 'L6'],
    "P8": ['L2', 'L3', 'L6']
}



def calculate_mask(target: str, mask: str, mode: str) -> list:
    target_traits = Persona.get(target, [])
    mask_traits = Persona.get(mask, [])
    if mode == "U":
        return list(set(target_traits) | set(mask_traits))
    elif mode == "I":
        return list(set(target_traits) & set(mask_traits))
    elif mode == "D":
        return list(set(target_traits) - set(mask_traits))
    else:
        return target_traits
    

async def test(message: str, sex: str, age: str, story: str, target: str, mask: str, mode: str, patience: int):
    async with httpx.AsyncClient() as client:
        data = {
            "content": message,
            "age": age,
            "sex": sex,
            "story": story,
            "traits": calculate_mask(target, mask, mode),
            "patience": patience
        }
        print("请求中")
        try:
            # 发送异步 POST 请求
            response = await client.post("http://localhost:8000/api/chat", json=data, timeout=60.0)
            
            if response.status_code != 200:
                return f"Error {response.status_code}: {response.text}"
            
    
            reply_json = json.loads(response.json().get("reply", "{}"))
            if not game_mode:
                print(reply_json)

            patience = reply_json.get("patience")
            active_traits = reply_json.get("active_traits", [])
            content = reply_json.get("content", "")
            
            print(f"\n回复: {content}")
            print(f"触发正向特质: {active_traits}")
            print(f"当前耐心值: {patience}")
            return 
        except Exception as e:
            print(f"请求异常: {str(e)}")


    
def init_story(sex: str, age: str):
    with httpx.Client() as client:
        data = {
            "age": age,
            "sex": sex,
            "traits": target_traits
        }
        print("人物生成中")
        try:
            response = client.post("http://localhost:8000/api/story", json=data, timeout=60.0)
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
            
            reply_json = json.loads(response.json().get("reply", "{}"))
            if not game_mode:
                print(reply_json)

            global story
            story = reply_json.get("story", "")
            print(f"初始化背景故事完成:\n{story}\n")
            return
        except Exception as e:
            print(f"请求异常: {str(e)}")


if __name__ == "__main__":
    patience = 100
    story = ""
    game_mode = False

    target = input("请选择对话角色人格 (P1 - P8, 若不输入则随机生成，随后仅展示对话内容以及触发特质): ")
    if not target:
        game_mode = True
        target = random.choice(list(Persona.keys()))

    target_traits = Persona.get(target, [])
    sex = input("请输入角色性别 (male/female): ")
    age = input("请输入角色年龄: ")
    init_story(sex=sex, age=age)
    while(True):
        mask_string = input("\n请输入面具，如\"P1U\", \"P2I\", U表示并集，I表示交集。如果仅输入\"P1\"则表示猜测人格 (或输入 'exit' 退出): ")
        if len(mask_string) == 2 and mask_string == target:
            print("恭喜你，猜对了角色人格!")
            exit(0)
        else:
            print("猜错了，继续加油!")
        input_message = input("请输入问题: ")
        if mask_string.lower() == 'exit':
            break
        result = asyncio.run(test(
            message=input_message,
            sex=sex, age=age, 
            story=story, 
            target=target, 
            mask=mask_string[:2], 
            mode=mask_string[2:], 
            patience=patience))
 