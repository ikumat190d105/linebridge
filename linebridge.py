#coding: utf-8

import json
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#ゲートウェイの情報の取得
linebridge_file = open('gateway.json', 'r')
linebridge_info = json.load(linebridge_file)

#ユーザーIDやトークンを取得
setting_file = open('setting.json', 'r')
setteing_info = json.load(setting_file)

CHANNEL_ACCESS_TOKEN = setteing_info["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

#取得した情報からメッセージのやり取りをするためのURLを作成
url = setteing_info["URL"]
stream_url = url + '/api/stream'
messages_url = url + '/api/messages'

def main():

    print("プログラムを開始します")

    #r = requests.get(messages_url)
    while True:
        try:
            r = requests.get(stream_url, stream=True)

            #メッセージを取得したとき、LINEにメッセージを送信する
            for msg in r.iter_lines():
                if msg:
                    print(msg)
                    jmsg = json.loads(msg)

                    if jmsg["gateway"] == "":
                        continue

                    if jmsg["text"]:
                        print("-----------------------------------")
                        print("テキスト　：" + jmsg["text"])
                        print("ユーザー　：" + jmsg["username"])
                        print("プロトコル：" + jmsg["protocol"])
                        print("ゲート　　：" + jmsg["gateway"])
                        print("-----------------------------------")

                        try:
                            gateway = jmsg["gateway"]
                            GROUP_ID = linebridge_info[gateway] #LINEグループのグループIDを取得
                            to = GROUP_ID
                            messages = TextSendMessage(text = "[" + jmsg["protocol"] + "] " + "<" + jmsg["username"] + "> \n" + jmsg["text"])
                        
                        except:
                            USER_ID = setteing_info["USER_ID"]
                            to = USER_ID
                            messages = TextSendMessage(text = "設定されてないゲートウェイからメッセージです\nUser = " + jmsg["username"] + "\nGateway = " + jmsg["gateway"] + "\nmessage = " + jmsg["text"])
                        
                        line_bot_api.push_message(to, messages = messages)
                                  
        except:
            print("プログラムを終了します")
            break


if __name__ == "__main__":
    main()

