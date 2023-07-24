import boto3
from boto3.dynamodb.conditions import Key


bucket_name = 'samsung-icn-moneybook-bucket'  # S3 버킷 이름
csv_file_name = 'moneybook.csv'  # 가져올 파일 이름

def lambda_handler(event, context):

    #변경할 데이터 가져오기
    user = event['User']
    date = event['Date']
    changes = event['Changes']
    update_data = event['Update_data']

    if changes =="Category":
        update_data = "지출" if update_data == "수입" else "지출"

    # 업데이트할 데이터 정보
    update_expression = f"SET {changes} = :value"
    expression_attribute_values = {
        ':value': update_data  # 업데이트할 값
    }

    # AWS SDK 클라이언트 생성
    dynamodb = boto3.resource('dynamodb')
    
    # DynamoDB 테이블 정보
    table = dynamodb.Table('Moneybook')
    
    try:
        response = table.update_item(
            Key={
                'User' : user,
                'Date' : date
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )

    except Exception as e:
        # 업데이트 실패시 예외 처리
        response = table.query(KeyConditionExpression=Key('User').eq(user))
        items = response['Items']
        return {
            'statusCode': 500,
            'body': str(e)
        }
    
    else :
        response = table.query(KeyConditionExpression=Key('User').eq(user))
        items = response['Items']
        return items