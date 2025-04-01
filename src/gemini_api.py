import requests
import json
import re
from src.config import API_KEY, GEMINI_API_URL_BASE, GEMINI_WAIT_TIME_PER_CHAR, GEMINI_WAIT_TIME_ADDITIONAL
from src.history import add_to_history, conversation_history
import time
import asyncio
import html #追加

MY_NAME = "自身"  # 自身の名前
CONVERSATION_PARTNER_NAME = "会話相手" #会話相手の名前

def escape_html(text):
    """HTML エスケープを行います。"""
    return html.escape(text)

def get_gemini_response(api_key, prompt):
    """Gemini API にリクエストを送信し、応答を取得します。"""
    if not api_key:
        print("エラー: APIキーが設定されていません。")
        return None, "APIキーエラー"

    url = f"{GEMINI_API_URL_BASE}?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # ステータスコードが 200 以外の場合は例外を発生させる
        response_json = response.json()

        if 'candidates' not in response_json:
            return None, "APIレスポンスエラー"

        if not response_json['candidates']:
             return None, "APIレスポンスエラー"

        if 'content' not in response_json['candidates'][0]:
             return None, "APIレスポンスエラー"

        if 'parts' not in response_json['candidates'][0]['content']:
             return None, "APIレスポンスエラー"

        if 'text' not in response_json['candidates'][0]['content']['parts'][0]:
             return None, "APIレスポンスエラー"

        generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
        return generated_text, None

    except requests.exceptions.RequestException as e:
        print(f"エラー: API リクエスト中にエラーが発生しました: {e}")
        return None, "APIリクエストエラー"
    except json.JSONDecodeError as e:
        print(f"エラー: JSON デコード中にエラーが発生しました: {e}")
        return None, "APIレスポンスエラー"
    except Exception as e:
        print(f"エラー: その他のエラーが発生しました: {e}")
        return None, "GeminiAPIエラー"

def handle_gemini_response(gemini_response):
  """GeminiAPIの処理を行います"""
  print(f"Gemini APIからの応答: {gemini_response}")
  # コンソールに出力
  print(f"コンソール出力: {gemini_response}")
  # 感嘆符が含まれている場合は削除
  gemini_response = re.sub(r'!', '', gemini_response)
  # _が含まれている場合スペースに戻す
  gemini_response = re.sub(r'_', ' ', gemini_response)
  #HTMLエスケープ
  gemini_response = escape_html(gemini_response) #追加

  return gemini_response

def send_gemini_prompt(persona_text,input_text, conversation_history,conversation_partner,my_name):
    """GeminiAPIに送信する処理を行います"""
    # 会話履歴をプロンプトに追加
    history_text = ""
    if conversation_history:
        history_text += "以下は、今までの会話内容です。\n\n会話履歴:\n"
        for item in conversation_history:
            history_text += f"{item['speaker']}: {escape_html(item['text'])}\n" #変更箇所
        history_text += "\n"
    #HTMLエスケープ
    persona_text = escape_html(persona_text)
    input_text = escape_html(input_text)

    gemini_prompt = f"{persona_text}\n\n{history_text}\n\n現在の会話:\n{conversation_partner}: {input_text}\n{my_name}:"
    gemini_response, error_message = get_gemini_response(API_KEY, gemini_prompt)
    return gemini_response, error_message

def gemini_worker(input_text, persona_text, conversation_history,websocket_port,send_text_to_websocket,bouyomi_port,bouyomi_talk,conversation_partner):
    """GeminiAPIとの処理を実行します"""
    if persona_text is None:
        return

    gemini_response, error_message = send_gemini_prompt(persona_text,input_text,conversation_history,conversation_partner,MY_NAME)

    if gemini_response:
        text = handle_gemini_response(gemini_response)
        # 会話履歴の更新(Geminiの応答)
        add_to_history(MY_NAME, text)

        send_text = asyncio.run(send_text_to_websocket(websocket_port, text))
        if send_text:
          time.sleep(len(send_text) * GEMINI_WAIT_TIME_PER_CHAR + GEMINI_WAIT_TIME_ADDITIONAL)
