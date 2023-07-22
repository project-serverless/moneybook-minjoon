import boto3
import os
import io
import pandas as pd
import csv

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def lambda_handler(event, context):

    #변경할 데이터 가져오기
    modify_index = event['modify_index']
    changes = event['changes']
    modify_data = event['modify_data']

    #s3 버킷에서 csv 데이터 가져오기
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name,Key=csv_file_name)
    csv_data = response["Body"].read().decode("utf-8")

    #csv 데이터를 데이터프레임으로 변환
    data = pd.read_csv(io.StringIO(csv_data))

    idx= int(modify_index-1)

    #원하는 데이터 수정
    if changes=="금액":
        data.loc[idx,changes] = int(modify_data)
    else:
        data.loc[idx,changes] = modify_data
    
    #csv 데이터로 변환
    csv_data = data.to_csv(index=False, encoding='utf-8')
    
    #s3 버켓에 파일 덮어쓰기
    s3_client.put_object(Bucket = bucket_name, Key=csv_file_name,Body=csv_data)

    return {
        "statusCode": 200,
        "body": "데이터가 성공적으로 수정되었습니다."
    }

