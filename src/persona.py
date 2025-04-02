def load_persona_data(persona_file_path):
    """persona.ini ファイルから設定を読み込みます。"""
    try:
        with open(persona_file_path, "r", encoding="utf-8") as f:
            persona_text = f.read()
            return persona_text
    except FileNotFoundError:
        print(f"エラー: persona.ini ファイルが見つかりません。パスを確認してください: {persona_file_path}")
        return None
