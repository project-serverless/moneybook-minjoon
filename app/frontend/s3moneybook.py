import dotenv

dotenv.load_dotenv(".env", override=True)

import json
import boto3
import gradio as gr
import pandas as pd

#조회 함수  

def json_pandas(json_string):
    json_data = json.loads(json_string)
    data = pd.read_json(json_data)
    return data
 
def read__csv():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName= 'SAMSUNG-ICN-read-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                        })
                    )
    if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        print(data_json)
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None

#삭제 함수
def delete_csv(delete_index):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='SAMSUNG-ICN-delete-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "delete_index": delete_index
                        })
                    )
    if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        print(data_json)
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None

#수정 함수
def update_csv(modify_index,changes,modify_data):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='SAMSUNG-ICN-update-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "modify_index" : modify_index,
                            "changes" : changes,
                            "modify_data" : modify_data
                        })
                    )
    if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        print(data_json)
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None
    
def create_csv(category,purpose,amount=0,memo=""):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='SAMSUNG-ICN-create-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "Category" : category,
                            "Purpose" : purpose,
                            "Amount" : amount,
                            "Memo" : memo
                        })
                    )
    return True

#출력 함수
with gr.Blocks() as moneyBook:
    gr.Markdown("가계부 어플리케이션")
    with gr.Tab("입력"):
        create_input = [
            gr.Dropdown(choices=["수입", "지출"], label="Category"),
            gr.Textbox(label="Purpose"),
            gr.Number(label="Amount"),
            gr.inputs.Textbox(label="Memo"),
        ]
        create_button = gr.Button("입력")
        
    with gr.Tab("조회"):
        read_button = gr.Button("조회")
        read_output = gr.outputs.Dataframe(type="pandas",label="목록")
        delete_inputs = gr.Number(label="delete_index")
        delete_button = gr.Button("삭제")
        update_inputs = [ 
                gr.Number(label="modify_index"),
                gr.Dropdown(choices=["Category","Purpose","Amount","Memo"],label="changes"),
                gr.Textbox(label="modify_data")
        ]
        update_button = gr.Button("수정")  
       
    create_button.click(create_csv, inputs=create_input, outputs=[])
    read_button.click(read__csv, inputs=[], outputs=read_output)
    update_button.click(update_csv,inputs=update_inputs,outputs=read_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=read_output)
    
moneyBook.launch()
