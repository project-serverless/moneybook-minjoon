import boto3
import os
import io
import pandas as pd

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def lambda_handler(event, context):

    #삭제할 인덱스 데이터 가져오기
    delete_index = event['delete_index']

    #s3 버킷에서 csv 데이터 가져오기
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name,Key=csv_file_name)
    csv_data = response["Body"].read().decode("utf-8")

    #csv 데이터를 데이터프레임으로 변환
    data = pd.read_csv(io.StringIO(csv_data))

    #해당 인덱스 삭제
    data.drop(delete_index-1,inplace=True)
    
    #csv 데이터로 변환
    csv_data = data.to_csv(index=False, encoding='utf-8')
    
    #s3 버켓에 파일 덮어쓰기
    s3_client.put_object(Bucket = bucket_name, Key=csv_file_name,Body=csv_data)
 
    return data.to_json(orient='records')


