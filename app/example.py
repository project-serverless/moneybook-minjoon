import gradio as gr
import datetime
import pandas as pd
import csv

#계산기, 메모장, 통계 기능

coin = 0

def calc(symbol,useMoney):
    if symbol == "+":
        result = coin+useMoney
    elif symbol == "-":
        result = coin-useMoney                   
    return result    

#데이터 입력 함수   
def write_csv(transaction):
    file_path = "AccountBook_output.csv"
    f= open(file_path,'a')
    writer = csv.writer(f)
    writer.writerows(transaction)
    f.close()

#조회 함수  
def read__csv():
    data = pd.read_csv("AccountBook_output.csv",encoding= 'utf-8')
    data=data.fillna(0)
    return data

#삭제 함수
def delete_csv(delete_index):
    data = pd.read_csv("AccountBook_output.csv",encoding= 'utf-8')
    data.drop(delete_index-1,inplace=True)
    data.to_csv("AccountBook_output.csv", index=False, encoding='utf-8')
    return data

#수정 함수
def modify_csv(modify_index,changes,modify_data):
    global coin
    data = pd.read_csv("AccountBook_output.csv",encoding= 'utf-8')
    idx= int(modify_index-1)
    md = modify_data
    #"Category","목적","사용내역","금액","Meno"
    if changes=="금액":
        coin = coin - data.loc[idx,changes]
        data.loc[idx,changes] = int(md)
        coin = coin + data.loc[idx,changes]
    elif changes == "Category":
        coin = coin - 2*data.loc[idx,"금액"]
        data.loc[idx,changes] = md
    else:
        data.loc[idx,changes] = md
        
    data.to_csv("AccountBook_output.csv", index=False, encoding='utf-8')
    return data
    
def input_main(category,purpose,name,amount=0,memo=""):
        global coin
        transaction = []
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    
        if category == "수입":
            coin = coin+amount
        elif category == "지출":
            coin = coin-amount
    
        transaction.append([date,category,purpose,name,amount,memo,coin])
        write_csv(transaction)
    
        data = pd.read_csv("AccountBook_output.csv",encoding= 'utf-8')
        data=data.fillna(0)
        return data

#출력 함수
with gr.Blocks() as asdf:
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

   # with gr.Tab("수정"):
    #    modify_output = [gr.outputs.Dataframe(type="pandas",label="목록")]
        
            
    record_button.click(input_main, inputs=text_input, outputs=[])
    print_button.click(read__csv, inputs=[], outputs=print_output)
    modify_button.click(modify_csv,inputs=modify_inputs,outputs=print_output)
    delete_button.click(delete_csv,inputs=delete_inputs,outputs=print_output)
    
asdf.launch()
