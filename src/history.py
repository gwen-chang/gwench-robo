from src.config import get_config_value

conversation_history = []

def add_to_history(speaker, text):
    """会話履歴にメッセージを追加します。"""
    global conversation_history
    try:
        conversation_history.append({"speaker": speaker, "text": text})
        # 最大保持件数を超えた場合、古い履歴を削除
        if len(conversation_history) > get_config_value('MAX_HISTORY_LENGTH'): #修正箇所
            conversation_history.pop(0)
        print(f"会話履歴を更新しました: {conversation_history}")
    except Exception as e:
        print(f"会話履歴の更新中にエラーが発生しました: {e}")

def clear_history():
    """会話履歴をクリアします。"""
    global conversation_history
    conversation_history = []
    print("会話履歴をクリアしました。")
