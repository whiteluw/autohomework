import pyaudio
import wave
import os
import speech_recognition as sr
from pynput.keyboard import Key, Controller
import requests
import time

# 百度翻译API信息
api_url = "https://api.fanyi.baidu.com/api/trans/vip/translate"
app_id = ""
api_key = ""

# 初始化键盘控制器
keyboard = Controller()

# 录音参数
chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100
record_seconds = 3

# 初始化语音识别器
recognizer = sr.Recognizer()

# 初始化Pyaudio
p = pyaudio.PyAudio()

# 录音函数
def record_audio(wave_output_filename):
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("* 正在录音")
    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("* 录音结束")

    stream.stop_stream()
    stream.close()

    wf = wave.open(wave_output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# 语音转文字函数
def speech_to_text(audio_filename):
    with sr.AudioFile(audio_filename) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

# 文字翻译函数
def translate_text(text, src_lang, dest_lang):
    params = {
        'q': text,
        'from': src_lang,
        'to': dest_lang,
        'appid': app_id,
        'salt': str(time.time()),
        'sign': create_sign(text, app_id, api_key)
    }
    response = requests.get(api_url, params=params)
    result = response.json()
    return result['trans_result'][0]['dst']

# 创建翻译签名
def create_sign(q, appid, key):
    import hashlib
    salt = str(time.time())
    sign = hashlib.md5((appid + q + salt + key).encode('utf-8')).hexdigest()
    return sign

# 模拟键盘输入函数
def simulate_typing(input_text):
    keyboard.type(input_text)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)

# 主循环
while True:
    audio_filename = "temp_audio.wav"
    record_audio(audio_filename)
    text = speech_to_text(audio_filename)
    simulate_typing(text)
    translated_text = translate_text(text, 'en', 'zh')
    simulate_typing(translated_text)
