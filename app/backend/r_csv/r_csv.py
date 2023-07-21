
import boto3
import pandas as pd

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

#버킷으로 부터 파일 저장
def download_file_from_s3(bucket_name, s3_key):
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, s3_key, csv_file_name)

def lambda_handler(event, context):
    download_file_from_s3(bucket_name,csv_file_name)
    data = pd.read_csv(csv_file_name,encoding= 'utf-8')
    data=data.fillna(0)
    return data

