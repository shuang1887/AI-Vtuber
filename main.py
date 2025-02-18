import requests
import time
from pydub import AudioSegment
from pydub.playback import play
import io

# -------------------------------------------COZE api 初始化---------------------------------------------------
personal_access_token = ''
bot_id = ''

# 构造请求头
header = {
    'Authorization': f'Bearer {personal_access_token}',
    'Content-Type': 'application/json'
}
url_vits = "http://127.0.0.1:9880/tts"

# 定义获取回复文本的函数
def get_response(chat_id, conversation_id):
    template_response = 'https://api.coze.cn/v3/chat/message/list?chat_id={}&conversation_id={}'
    url_response = template_response.format(chat_id, conversation_id)

    response = requests.get(url_response, headers=header)
    if response.ok:
        response_data = response.json()
        return response_data['data'][0]['content']
    else:
        print('获取回复失败，状态码：', response.status_code)
        print('错误信息：', response.text)
        return None


# 定义监控对话状态的函数
def monitor(chat_id, conversation_id):
    template_retrieve = 'https://api.coze.cn/v3/chat/retrieve?chat_id={}&conversation_id={}'
    url_retrieve = template_retrieve.format(chat_id, conversation_id)

    while True:
        chat_object = requests.get(url_retrieve, headers=header)
        if chat_object.ok:
            chat_object_content = chat_object.json()
            if chat_object_content['data']['status'] == 'completed':
                break
        else:
            print('监控失败，状态码：', chat_object.status_code)
        time.sleep(1)


# -------------------------------------------多轮对话逻辑---------------------------------------------------
def main():
    conversation_id = None
    while True:
        # 获取用户输入
        user_input = input("你：")
        if user_input.lower() in ['退出', 'exit', 'quit']:
            print("对话已结束。")
            break

        # 构造请求体
        body_chat = {
            'bot_id': bot_id,
            'user_id': 'testUser',
            'stream': False,
            'additional_messages': [
                {
                    'role': 'user',
                    'content': user_input,
                    'content_type': 'text'
                }
            ]
        }

        # 创建或继续对话，发送POST请求
        template_conadd = 'https://api.coze.cn/v3/chat'
        if conversation_id is not None:
            body_chat['conversation_id'] = conversation_id
            url_conadd = template_conadd + '?' + 'conversation_id=' + conversation_id
        else:
            url_conadd = template_conadd
        post_message_chat = requests.post(
            url_conadd,
            headers=header,
            json=body_chat
        )

        if post_message_chat.ok:
            print("请求已发送。")
            post_message_chat_data = post_message_chat.json()
            chat_id = post_message_chat_data['data']['id']
            conversation_id = post_message_chat_data['data']['conversation_id']

            # 监控对话状态
            monitor(chat_id, conversation_id)

            # 获取回复文本,并转换为lulu音色(模型自己训练，参数需自己填写）
            bot_reply = get_response(chat_id, conversation_id)
            body_vits = {
                "text": bot_reply,
                "text_lang": "zh",
                "ref_audio_path": "",
                "aux_ref_audio_paths": [],
                "prompt_text": "",
                "prompt_lang": "zh",
                "top_k": 5,
                "top_p": 1,
                "temperature": 1,
                "text_split_method": "cut0",
                "batch_size": 1,
                "batch_threshold": 0.75,
                "split_bucket": True,
                "return_fragment": False,
                "speed_factor": 1.0,
                "streaming_mode": False,
                "seed": -1,
                "parallel_infer": True,
                "repetition_penalty": 1.35
            }
            if bot_reply:
                post_message_vits = requests.post(url_vits, json=body_vits)
                if post_message_vits.ok:
                    print("gpt-sovits api请求成功")
                    audio_data = io.BytesIO(post_message_vits.content)
                    audio = AudioSegment.from_file(audio_data, format="wav")
                    print(f"AI-lulu：{bot_reply}")
                    play(audio)
                else:
                    print("gpt-sovits api请求失败")
                    print('错误信息：', post_message_vits.text)
        else:
            print('Coze api请求失败，状态码：', post_message_chat.status_code)
            print('错误信息：', post_message_chat.text)


if __name__ == "__main__":
    main()
