import datetime
import pandas as pd
import csv
import boto3
import io

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def lambda_handler(event, context):

    #받아온 데이터
    data = {
        'Date': [datetime.datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분%S초')],
        'Category': [event.get('Category', '')],
        'Purpose': [event.get('Purpose', '')],
        'Amount': [event.get('Amount', 0)],
        'Memo': [event.get('Memo', '')]
    }
    df = pd.DataFrame(data)

    # S3 버킷에서 데이터 가져오기
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket= bucket_name,Key = csv_file_name)
    csv_data = response["Body"].read().decode("utf-8")

    # 기존 CSV 데이터를 데이터프레임으로 변환
    df_existing = pd.read_csv(io.StringIO(csv_data))

    # 새로운 데이터를 포함하여 데이터프레임에 추가
    new_df = pd.concat([df_existing,df])

    # 데이터프레임을 CSV 형식의 문자열로 변환
    csv_data = new_df.to_csv(index=False)

    #s3 버켓에 파일 덮어쓰기
    s3_client.put_object(Bucket = bucket_name, Key=csv_file_name,Body=csv_data)

    return {
        "statusCode": 200,
        "body": "데이터가 성공적으로 입력되었습니다."
    }

