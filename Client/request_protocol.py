from config import *


class RequestProtocol(object):
    @staticmethod
    def request_login_result(username, password):
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat(username, message):
        return DELIMITER.join([REQUEST_CHAT, username, message])

    @staticmethod
    def request_send_file(username, file_name):
        return DELIMITER.join([REQUEST_SEND_FILE, username, file_name])

    @staticmethod
    def request_audio_setting(username):
        return DELIMITER.join([REQUEST_AUDIO_SETTING, username])

    @staticmethod
    def request_audio_close(username):
        return DELIMITER.join([REQUEST_AUDIO_CLOSE, username])

