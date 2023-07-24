import dotenv

dotenv.load_dotenv(".env", override=True)

import json
import boto3
import gradio as gr
import pandas as pd

#입력 함수
def create_csv(user,category,purpose,amount,memo):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='SAMSUNG-ICN-create-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "User" : user,
                            "Category" : category,
                            "Purpose" : purpose,
                            "Amount" : amount,
                            "Memo" : memo
                        })
                    )
    return True

#dynamodb를 pandas dataFrame으로 변환
def json_pandas(json_data):
    data = pd.read_json(json_data)
    return data

#조회 함수
def read__csv(User):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName= 'SAMSUNG-ICN-read-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "User" : User
                        })
                    )
    
    data_json = response['Payload'].read().decode('utf-8')
    return json_pandas(data_json)
    '''if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None'''

#삭제 함수
def delete_csv(User,Date):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='SAMSUNG-ICN-delete-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "User" : User,
                            "Date" : Date
                        })
                    )
    data_json = response['Payload'].read().decode('utf-8')
    return json_pandas(data_json)
    '''if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None'''

#수정 함수
def update_csv(User,Date,Changes,Update_data):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='SAMSUNG-ICN-update-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "User" : User,
                            "Date" : Date,
                            "Changes" : Changes,
                            "Update_data" : Update_data
                        })
                    )
    data_json = response['Payload'].read().decode('utf-8')
    return json_pandas(data_json)
    '''if response['StatusCode'] == 200:
        # Lambda 함수의 응답 데이터를 JSON으로 파싱하여 반환.
        data_json = response['Payload'].read().decode('utf-8')
        return json_pandas(data_json)
    else:
        print("Lambda 함수 호출에 실패했습니다!")
        return None'''
    


#홈페이지 탭
with gr.Blocks() as moneyBook:
    gr.Markdown("가계부 어플리케이션")
    with gr.Tab("입력"):
        create_input = [
            gr.Textbox(label="user"),
            gr.Dropdown(choices=["수입", "지출"], label="category"),
            gr.Textbox(label="purpose"),
            gr.Textbox(label="amount"),
            gr.Textbox(label="memo"),
        ]
        create_button = gr.Button("입력")
        
    with gr.Tab("조회"):
        read_button = gr.Button("조회")
        read_input = gr.Textbox(label="User")
        read_output = gr.outputs.Dataframe(type="pandas",label="목록")
        delete_inputs = [
            gr.Textbox(label="User"),
            gr.Textbox(label="Date")
        ]
        delete_button = gr.Button("삭제")
        update_inputs = [ 
            gr.Textbox(label="User"),
            gr.Textbox(label="Date"),
            gr.Dropdown(choices=["Category","Purpose","Amount","Memo"],label="Changes"),
            gr.Textbox(label="Modify_data")
        ]
        update_button = gr.Button("수정")  
       
    #버튼 목록
    create_button.click(create_csv, inputs=create_input, outputs=[])
    read_button.click(read__csv, inputs=read_input, outputs=read_output)
    update_button.click(update_csv,inputs=update_inputs,outputs=read_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=read_output)

#인터페이스 실행
moneyBook.launch()
