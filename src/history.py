from src.config import MAX_HISTORY_LENGTH
import html #追加

def escape_html(text):
    """HTML エスケープを行います。"""
    return html.escape(text)

conversation_history = []

def add_to_history(speaker, text):
    """会話履歴にメッセージを追加します。"""
    global conversation_history
    try:
        text = escape_html(text) #追加
        conversation_history.append({"speaker": speaker, "text": text})
        # 最大保持件数を超えた場合、古い履歴を削除
        if len(conversation_history) > MAX_HISTORY_LENGTH:
            conversation_history.pop(0)
        print(f"会話履歴を更新しました: {conversation_history}")
    except Exception as e:
        print(f"会話履歴の更新中にエラーが発生しました: {e}")
