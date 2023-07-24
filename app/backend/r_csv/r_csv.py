import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    
   #이벤트 데이터 받아오기
   user = event['User']
   
   #AWS SDK 클라이언트 생성
   dynamodb = boto3.resource('dynamodb')
    
   #db table 정보
   table = dynamodb.Table('Moneybook')

   #해당 USER 조회 후 데이터 변수에 저장
   response = table.query(KeyConditionExpression=Key('User').eq(user))   
   items = response['Items']
   
   return items

