import boto3
import pandas as pd
import io

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름


def lambda_handler(event, context):

    #s3 버킷에서 csv 데이터 가져오기
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name,Key=csv_file_name)
    data = response["Body"].read().decode("utf-8")

    #데이터 프레임으로 변경, 빈칸은 0으로 채우고 전달
    data = pd.read_csv(io.StringIO(data))

    return data.to_json(orient='records')

