import boto3
import os
import logging
import pandas as pd

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

#버킷으로 부터 파일 저장
def download_file_from_s3(bucket_name, s3_key):
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, s3_key, csv_file_name)

#버킷으로 파일 업로드
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

def lambda_handler(event, context):
    #버킷으로 부터 파일 저장
    download_file_from_s3(bucket_name,csv_file_name)

    delete_index = event['delete_index']
    data = pd.read_csv(csv_file_name,encoding= 'utf-8')
    data.drop(delete_index-1,inplace=True)
    data.to_csv(csv_file_name, index=False, encoding='utf-8')
    
    upload_file(csv_file_name, bucket_name, csv_file_name)
    
    return data


