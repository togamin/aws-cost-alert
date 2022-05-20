import os
import json
import requests

#環境変数からSlackに通知するためのURLを取得
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def post_slack(event, context) -> None:
    #通知内容の設定
    payload = {
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': 'Hello Slack!!',
                'text': 'LamdaからSlackへ通知テスト'
            }
        ]
    }
    # Slackへのリクエストの作成と通知
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)