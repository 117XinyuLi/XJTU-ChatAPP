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

# 服务器相关配置
SERVER_IP = '127.0.0.1'  # 服务器IP
SERVER_PORT = 8090  # 服务器端口
AUDIO_PORT = 9808  # 语音端口
FILE_PORT = 8091  # 文件传输端口

# 数据库相关配置
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'mini_chat'
DB_USER = 'root'
DB_PASSWORD = '你的密码'

# 文件存储路径
FILE_PATH = 'files'  # 文件存储路径
END_OF_SEND = b'\x00'  # 文件发送结束标志



