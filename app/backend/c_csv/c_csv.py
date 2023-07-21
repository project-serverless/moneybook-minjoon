import datetime
import pandas as pd
import csv
import boto3
import os
import logging


s3 = boto3.client('s3')
bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def download_file_from_s3(bucket_name, s3_key):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, csv_file_name)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def append_csv(transaction):
    f= open(csv_file_name,'a')
    writer = csv.writer(f)
    writer.writerows(transaction)
    f.close()

def lambda_handler(event, context):

    # S3 버킷에서 파일 가져오기
    download_file_from_s3(bucket_name,csv_file_name)

    category = event['category']
    purpose = event.get('purpose','')
    amount = event.get('amount', 0)  # amount 값이 없을 경우 기본값으로 0 설정
    memo = event.get('memo', '')

    transaction = []
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    transaction.append([date, category, purpose, amount, memo])
    append_csv(transaction)

    data = pd.read_csv(csv_file_name,encoding= 'utf-8')
    data=data.fillna(0)

    upload_file(csv_file_name,bucket_name,csv_file_name)

    return data

