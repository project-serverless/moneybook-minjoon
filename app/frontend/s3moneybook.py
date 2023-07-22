import dotenv

dotenv.load_dotenv(".env", override=True)

import json
import boto3
import gradio as gr
import pandas as pd

#조회 함수  

def json_pandas():
    json_data = read__csv()
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
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환합니다.
        data_json = response['Payload'].read().decode('utf-8')
        print(data_json)
        return data_json
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None

#삭제 함수
def delete_csv(delete_index):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='SAMSUNG-ICN-delete-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "delete_index": delete_index
                        })
                    )
    return True

#수정 함수
def update_csv(modify_index,changes,modify_data):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='SAMSUNG-ICN-update-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "modify_index" : modify_index,
                            "changes" : changes,
                            "modify_data" : modify_data
                        })
                    )
    return True
    
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
        text_input = [
            gr.Dropdown(choices=["수입", "지출"], label="Category"),
            gr.Textbox(label="Purpose"),
            gr.Number(label="Amount"),
            gr.inputs.Textbox(label="Memo"),
        ]
        record_button = gr.Button("입력")
        
    with gr.Tab("조회"):
        print_button = gr.Button("조회")
        print_output = gr.outputs.Dataframe(type="pandas",label="목록")
        delete_inputs = gr.Number(label="delete_index")
        delete_button = gr.Button("삭제")
        modify_inputs = [ 
                gr.Number(label="modify_index"),
                gr.Dropdown(choices=["Category","목적","금액","Meno"],label="changes"),
                gr.Textbox(label="modify_data")
        ]
        modify_button = gr.Button("수정")  
       
    record_button.click(create_csv, inputs=text_input, outputs=[])
    print_button.click(read__csv, inputs=[], outputs=print_output)
    modify_button.click(update_csv,inputs=modify_inputs,outputs=print_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=print_output)
    
moneyBook.launch()
