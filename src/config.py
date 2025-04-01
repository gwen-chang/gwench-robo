import configparser
import os

def load_config(file_path='config.ini'):
    """設定ファイルを読み込みます。"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    config_data = {}
    config_data['HTTP_PORT'] = int(config['DEFAULT']['http_port'])
    config_data['BOUYOMI_PORT'] = int(config['DEFAULT']['bouyomi_port'])
    config_data['API_KEY_CONFIG'] = config['DEFAULT']['api_key'] #修正
    config_data['PERSONA_FILE_PATH'] = config['DEFAULT']['persona_file_path']
    config_data['BOUYOMI_WAIT_TIME_PER_CHAR'] = float(config['DEFAULT']['bouyomi_wait_time_per_char'])
    config_data['BOUYOMI_WAIT_TIME_ADDITIONAL'] = float(config['DEFAULT']['bouyomi_wait_time_additional'])
    config_data['GEMINI_WAIT_TIME_PER_CHAR'] = float(config['DEFAULT']['gemini_wait_time_per_char'])
    config_data['GEMINI_WAIT_TIME_ADDITIONAL'] = float(config['DEFAULT']['gemini_wait_time_additional'])
    config_data['MAX_HISTORY_LENGTH'] = int(config['HISTORY']['max_history_length'])
    config_data['REGISTRY_KEY_PATH'] = config['WEB_SOCKET']['registry_key_path']
    config_data['REGISTRY_VALUE_NAME'] = config['WEB_SOCKET']['registry_value_name']
    config_data['WEBSOCKET_URI_FORMAT'] = config['WEB_SOCKET']['websocket_uri_format']
    config_data['GEMINI_API_URL_BASE'] = config['GEMINI_API']['gemini_api_url_base']

    return config_data

config_data = load_config()

HTTP_PORT = config_data['HTTP_PORT']
BOUYOMI_PORT = config_data['BOUYOMI_PORT']
API_KEY_CONFIG = config_data['API_KEY_CONFIG'] #修正
PERSONA_FILE_PATH = config_data['PERSONA_FILE_PATH']
BOUYOMI_WAIT_TIME_PER_CHAR = config_data['BOUYOMI_WAIT_TIME_PER_CHAR']
BOUYOMI_WAIT_TIME_ADDITIONAL = config_data['BOUYOMI_WAIT_TIME_ADDITIONAL']
GEMINI_WAIT_TIME_PER_CHAR = config_data['GEMINI_WAIT_TIME_PER_CHAR']
GEMINI_WAIT_TIME_ADDITIONAL = config_data['GEMINI_WAIT_TIME_ADDITIONAL']
MAX_HISTORY_LENGTH = config_data['MAX_HISTORY_LENGTH']
REGISTRY_KEY_PATH = config_data['REGISTRY_KEY_PATH']
REGISTRY_VALUE_NAME = config_data['REGISTRY_VALUE_NAME']
WEBSOCKET_URI_FORMAT = config_data['WEBSOCKET_URI_FORMAT']
GEMINI_API_URL_BASE = config_data['GEMINI_API_URL_BASE']

API_KEY = API_KEY_CONFIG #修正
