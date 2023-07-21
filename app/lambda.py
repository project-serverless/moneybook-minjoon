import dotenv 

dotenv.load_dotenv(".env",override=True)

import boto3
import json

def create_new_file(file_name):

    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='createCSVFile',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "file_name": file_name
                        })
                    )
    
    return True

create_new_file("money.csv")

''' def upload_file(file_name, bucket, object_name=None):
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



CSV_FILE = 'moneybook.csv'

#데이터 입력 함수   
def create_csv(transaction):
    f= open(CSV_FILE,'a')
    writer = csv.writer(f)
    writer.writerows(transaction)
    upload_file('moneybook.csv', 'moneybook-bucket-minjoon', 'moneybook.csv')
    f.close()

#조회 함수  
def read_csv():
    data = pd.read_csv(CSV_FILE,encoding= 'utf-8')
    data=data.fillna(0)
    return data

#삭제 함수
def delete_csv(delete_index):
    data = pd.read_csv(CSV_FILE,encoding= 'utf-8')
    data.drop(delete_index-1,inplace=True)
    data.to_csv(CSV_FILE, index=False, encoding='utf-8')
    upload_file('moneybook.csv', 'moneybook-bucket-minjoon', 'moneybook.csv')
    return data

#수정 함수
def update_csv(modify_index,changes,modify_data):
    data = pd.read_csv(CSV_FILE,encoding= 'utf-8')
    idx= int(modify_index-1)
    md = modify_data
    #"Category","목적","사용내역","금액","Meno"
    if changes=="금액":
        data.loc[idx,changes] = int(md)
    else:
        data.loc[idx,changes] = md
        
    data.to_csv(CSV_FILE, index=False, encoding='utf-8')
    upload_file('moneybook.csv', 'moneybook-bucket-minjoon', 'moneybook.csv')
    return data
    
def input_main(category,purpose,name,amount=0,memo=""):
        transaction = []
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        transaction.append([date,category,purpose,name,amount,memo])
        create_csv(transaction)
    
        data = pd.read_csv(CSV_FILE,encoding= 'utf-8')
        data=data.fillna(0)
        return data
'''