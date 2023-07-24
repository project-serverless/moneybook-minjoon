import datetime
import boto3

def lambda_handler(event, context):

    #받아온 데이터
    user = event['User']
    date = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분%S초')
    category = event.get('Category', '')
    purpose = event.get('Purpose', '')
    amount = event.get('Amount', 0)
    memo = event.get('Memo', '')
    
    #AWS SDK 클라이언트 생성
    dynamodb = boto3.resource('dynamodb')
    
    #db 테이블 정보
    table = dynamodb.Table('Moneybook')

    try:
        #테이블에 데이터 추가
        table.put_item(
            Item={
                'User' : user,
                'Date': date,
                'Category': category,
                'Purpose' : purpose,
                'Amount' : amount,
                'Memo' : memo
            })
        
    except Exception as e:
        #업데이트 실패시 예외 처리
        return {
            'statusCode': 500,
            'body': str(e)
        }

    return {
        "statusCode": 200,
        "body": "데이터가 성공적으로 입력되었습니다."
    }