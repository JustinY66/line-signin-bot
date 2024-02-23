from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import requests
import json

# 設定 Line Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('u8Ayn9wrrZpT1sCHH6WfAkbyEOmCL3G1mF/qc33/fcJt3lblNzzBPnY6cvc0y80zktfW3r8B6hSiS4jWLM+4JGfdHZDndVuwFlWiM2Hu4n5xUdT/tws0I9tbr4k71Tk3eY/AWBLc2c4k/quzUWUP+wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('43d88c1655651e6c934d561991554d0a')

app = Flask(__name__)

# 學生簽到紀錄，使用字典來保存
check_ins = {}

# Discord Webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1210240908000493588/TNGHAed-7tMbGiyXG6ZDv_LOOOZzdenO-6eZEQw1pcsp_zQh6evfjunFv05leD4DE8tT'

# 簽到的處理函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    if message_text.lower() == "簽到":
        if user_id in check_ins:
            reply_message = "你已經簽到過了！"
        else:
            # 在字典中紀錄簽到時間
            check_ins[user_id] = True
            reply_message = "簽到成功！"

            # 發送訊息到 Discord
            send_discord_message(f"使用者 {user_id} 簽到成功！")

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 發送訊息到 Discord 的函數
def send_discord_message(message):
    data = {
        'content': message
    }
    response = requests.post(discord_webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print('訊息已成功發送到 Discord!')
    else:
        print('發送訊息到 Discord 失敗！')

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 Line 傳遞過來的訊息
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']

    # 解析 Line 的訊息
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
