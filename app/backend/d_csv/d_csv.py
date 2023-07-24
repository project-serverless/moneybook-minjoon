import boto3
from boto3.dynamodb.conditions import Key

bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def lambda_handler(event, context):

    #받아온 데이터
    user = event['User']
    date = event['Date']

    #AWS SDK 클라이언트 생성
    dynamodb = boto3.resource('dynamodb')
    
    #db 테이블 정보
    table = dynamodb.Table('Moneybook')

    try:
        table.delete_item(Key={'User':user,'Date':date})

    except Exception as e:
        # 업데이트 실패시 예외 처리
        response = table.scan()
        items = response['Items']
        return {
            'statusCode': 500,
            'body': str(e)
        }
    
    else :
        response = table.query(KeyConditionExpression=Key('User').eq(user))
        items = response['Items']
        return items


