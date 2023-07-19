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