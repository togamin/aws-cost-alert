import os
import json
import requests

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def post_slack(event, context) -> None:
    payload = {
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': 'Hello Slack!!',
                'text': 'LamdaからSlackへ通知テスト'
            }
        ]
    }
    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)