import uuid
import json
import time
import requests

oaiDeviceId = None
token = None
updateTime = 0

def getTocken():
    global oaiDeviceId, token, updateTime
    while True:
        if time.time() - updateTime < 60:
            time.sleep(60)
        updateTime = time.time()
        try:
            random_uuid = str(uuid.uuid4())
            h = {
                "Oai-Device-Id": random_uuid,
                "Oai-Language": "en-US",
                "Origin": "https://chat.openai.com",
                "Referer": "https://chat.openai.com/",
                "Sec-Ch-Ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
            }
            response = requests.post(
            url= "https://chat.openai.com/backend-anon/sentinel/chat-requirements",
            data= {},
            headers= h
            )
            oaiDeviceId = random_uuid  
            token = json.loads(response.text)["token"]
            print("获取tocken成功！")
            return
        except:
            print("获取tocken失败，重新尝试中。。。")
            continue
    
def getQuestion(question):
    global oaiDeviceId, token
    while True:
        body = {
            "action": "next",
            "messages": [{"author": {"role": "user"},
                        "content": {"content_type": 'text', "parts": [question]}
                        }],
            "parent_message_id": str(uuid.uuid4()),
            "model": "text-davinci-002-render-sha",
            "timezone_offset_min": "-180",
            "suggestions": [],
            "history_and_training_disabled": True,
        " conversation_mode": { "kind": "primary_assistant" },
            "websocket_request_id": str(uuid.uuid4()),
        }
        h = {
            "oai-device-id": oaiDeviceId,
            "openai-sentinel-chat-requirements-token": token,
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Oai-Language": "en-US",
            "Origin": "https://chat.openai.com",
            "Referer": "https://chat.openai.com/",
            "Sec-Ch-Ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }
        response = requests.post(
            url= 'https://chat.openai.com/backend-api/conversation',
            data= json.dumps(body),
            headers= h,
            stream= True
        )
        if response.status_code == 200:
            break
        else:
            getTocken()
            continue
    ans = ""
    for message in response.iter_lines():
        parsed = eval(str(message)[1:])
        try:
            parsed = json.loads(parsed[5:])
        except:
            continue
        content = parsed.get("message", {}).get("content", {}).get("parts", [""])[0]
        if content == question or ans == content:
            continue
        ans = content
        yield content
        time.sleep(0.2)


if __name__ == '__main__':
    getTocken()
    print("-------------开始运行-------------")
    while True:
        q = input("问题：")
        a = getQuestion(q)
        for value in a:
            print(value,end = '\r回答： ')
        print()
        
