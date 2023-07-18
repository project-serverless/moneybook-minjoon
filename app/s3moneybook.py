import dotenv

dotenv.load_dotenv(".env", override=True)

import logging
import boto3
from botocore.exceptions import UnknownClientMethodError
import os
import gradio as gr
import datetime
import pandas as pd
import csv

def upload_file(file_name, bucket, object_name=None):
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

#출력 함수
with gr.Blocks() as moneyBook:
    gr.Markdown("가계부 어플리케이션")
    with gr.Tab("입력"):
        text_input = [
            gr.Dropdown(choices=["수입", "지출"], label="category"),
            gr.Textbox(label="purpose"),
            gr.Textbox(label="Name"),
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
                gr.Dropdown(choices=["Category","목적","사용내역","금액","Meno"],label="changes"),
                gr.Textbox(label="modify_data")
        ]
        modify_button = gr.Button("수정")  
       
    record_button.click(input_main, inputs=text_input, outputs=[])
    print_button.click(read_csv, inputs=[], outputs=print_output)
    modify_button.click(update_csv,inputs=modify_inputs,outputs=print_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=print_output)
    
moneyBook.launch()
