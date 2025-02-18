# AI-lulu
## What is it about
This project aims to create an AI Vtuber chatbot fufu (a fluffy doll) based on the real world Vtuber character: 雫るる (Shizuku Lulu). 
You will be able to chat with the fufu, and the fufu will interact with you in 雫るる's voice.

## Who is 雫るる (Shizuku Lulu)
雫るる (Shizuku Lulu) is one of the top Japanese Vtubers on bilibili, whose live stream features fluent Chinese and funny conversations.
Bilibili: https://space.bilibili.com/387636363

雫るる (Shizuku Lulu) has officially authorized the creation of non-commercial derivative works.

## Software
The software will incoporate LLMs to obtain multi-turn dialogue ability and will use Vits to achieve TTS with the user's favorate Vtuber's voice. For now, I have been using coze api and GPT-SoVits api for the LLM part and TTS part, separately.

## Hardware
The project aims to use esp-32 chips to achieve the realizations of a portable chatbot device. The chip will incoporate a sound receiver / speker to pick up user's voice and plays the AI 雫るる's voice, and a wifi module to send the voice to the server-end to generate answers and to transfer answer texts to the designated speech voices, and a memory chip to store the received data from server-end.

## Fufu design and manufacturing
To be decided.
