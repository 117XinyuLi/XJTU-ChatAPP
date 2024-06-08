SERVER_IP = '121.40.230.160'
SERVER_PORT = 8090
AUDIO_PORT = 9808  # 语音端口

REQUEST_LOGIN = '0001'  # 登录请求
REQUEST_CHAT = '0002'  # 聊天请求
REQUEST_SEND_FILE = '0003'  # 发送文件请求
REQUEST_AUDIO_SETTING = '0004'  # 音频设置
REQUEST_AUDIO_CLOSE = '0005'  # 音频数据


RESPONSE_LOGIN_RESULT = '1001'  # 登录结果
RESPONSE_CHAT = '1002'  # 聊天请求
RESPONSE_SEND_FILE = '1003'  # 发送文件结果
RESPONSE_AUDIO_SETTING = '1004'  # 音频设置
RESPONSE_AUDIO_CLOSE = '1005'  # 音频数据

DELIMITER = '|'  # 分隔符

# 文件存储路径
FILE_PATH = 'files'  # 文件存储路径
END_OF_SEND = b'\x00'  # 文件发送结束标志
FILE_PORT = 8091  # 文件传输端口

# 语音设置
import pyaudio
chunk_size = 1024  # 512
audio_format = pyaudio.paInt16
channels = 1
rate = 20000
