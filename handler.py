import os
import boto3
import json
import requests
from datetime import datetime, timedelta, date

#環境変数からSlackに通知するためのURLを取得
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def post_slack(event, context) -> None:

    # CostExplorer
    client = boto3.client('ce', region_name='us-east-1')

    # 対象月にかかったAWSの合計金額の算出
    total_billing = get_total_billing(client)

    # Slack通知内容の作成
    payload = {
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': '今月のAWS利用費用の合計金額',
                'text': '期間：' + total_billing['start']
                    + '〜' + total_billing['end']
                    + ' \n'
                    + '合計金額：' + str(round(float(total_billing['billing']), 2))
                    + '$'
            }
        ]
    }

    # Slackへの通知
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)

# 対象月にかかったAWSの合計金額の算出
def get_total_billing(client) -> dict:

    #コスト集計範囲の取得
    (start_date, end_date) = get_monthly_cost_date_range()

    #コスト集計範囲に対する合計コストの取得
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=[
            'AmortizedCost'
        ]
    )

    #取得したデータの返却
    return {
        'start': response['ResultsByTime'][0]['TimePeriod']['Start'],
        'end': response['ResultsByTime'][0]['TimePeriod']['End'],
        'billing': response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'],
    }

# 対象月のコスト算出対象の初日と当日の日付を取得する
def get_monthly_cost_date_range()->(str,str):

    # Costを算出する期間を設定する
    start_date = date.today().replace(day=1).isoformat()
    end_date = date.today().isoformat()

    # 「start_date」と「end_date」が同じ場合「start_date」は先月の月初の値を取得する。
    if start_date == end_date:
        end_of_month = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=-1)
        begin_of_month = end_of_month.replace(day=1)
        return begin_of_month.date().isoformat(), end_date

    return start_date, end_date