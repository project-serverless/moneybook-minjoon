import dotenv

dotenv.load_dotenv(".env", override=True)

import json
import boto3
import gradio as gr

#조회 함수  
def read_csv():

    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName= 'SAMSUNG-ICN-create-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                        })
                    )
    return True

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
    print(category,purpose,amount,memo)
    lambda_client.invoke(FunctionName='SAMSUNG-ICN-create-csv',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "category" : category,
                            "purpose" : purpose,
                            "amount" : amount,
                            "memo" : memo
                        })
                    )
    return True

#출력 함수
with gr.Blocks() as moneyBook:
    gr.Markdown("가계부 어플리케이션")
    with gr.Tab("입력"):
        text_input = [
            gr.Dropdown(choices=["수입", "지출"], label="category"),
            gr.Textbox(label="purpose"),
            gr.Number(label="Amount"),
            gr.inputs.Textbox(label="Memo"),
        ]
        record_button = gr.Button("입력")
        
    with gr.Tab("조회"):
        print_button = gr.Button("조회")
        print_output = [gr.outputs.Dataframe(type="pandas",label="목록")]
        delete_inputs = gr.Number(label="delete_index")
        delete_button = gr.Button("삭제")
        modify_inputs = [ 
                gr.Number(label="modify_index"),
                gr.Dropdown(choices=["Category","목적","금액","Meno"],label="changes"),
                gr.Textbox(label="modify_data")
        ]
        modify_button = gr.Button("수정")  
       
    record_button.click(create_csv, inputs=text_input, outputs=[])
    print_button.click(read_csv, inputs=[], outputs=print_output)
    modify_button.click(update_csv,inputs=modify_inputs,outputs=print_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=print_output)
    
moneyBook.launch()
