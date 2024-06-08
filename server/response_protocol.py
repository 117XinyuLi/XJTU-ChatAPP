from config import *


class ResponseProtocol(object):
    """Response Protocol class"""
    @staticmethod
    def response_login_result(result, nickname, username):
        """Response login result"""
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname, messages):
        """Response chat"""
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])

    @staticmethod
    def response_send_file(nickname, file_name):
        """Response send file"""
        return DELIMITER.join([RESPONSE_SEND_FILE, nickname, file_name])

    @staticmethod
    def response_audio_setting(nickname, ip, port):
        """Response audio setting"""
        return DELIMITER.join([RESPONSE_AUDIO_SETTING, nickname, ip, port])

    @staticmethod
    def response_audio_close(nickname):
        """Response audio"""
        return DELIMITER.join([RESPONSE_AUDIO_CLOSE, nickname])


