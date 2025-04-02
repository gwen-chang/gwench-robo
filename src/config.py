import configparser

def load_config(file_path='config.ini'):
    """設定ファイルを読み込みます。"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    config_data = {}
    config_data['HTTP_PORT'] = int(config['DEFAULT']['http_port'])
    config_data['BOUYOMI_PORT'] = int(config['DEFAULT']['bouyomi_port'])
    config_data['API_KEY_CONFIG'] = config['DEFAULT']['api_key']
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
    config_data['MAX_BOUYOMI_CHAR'] = int(config['DEFAULT']['max_bouyomi_char'])

    return config_data

def get_config_value(key):
    """設定ファイルから指定されたキーの値を取得します。"""
    config_data = load_config()
    return config_data.get(key)

def get_api_key():
    """APIキーを取得します。"""
    config_data = load_config()
    return config_data.get('API_KEY_CONFIG')
