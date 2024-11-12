#import library
from fastapi import FastAPI, HTTPException
import pandas as pd

# create instance/object
app = FastAPI()

@app.get("/")
def first_home():
    return "Hello"

@app.get("/data")
def get_data():
    df = pd.read_csv("data.csv")
    
    
    return df.to_dict(orient='records')

@app.get("/data/{id}")
def get_data_id(id: int):
    df = pd.read_csv("data.csv")
    # opsi untuk filter data -> df[kondisi] atau df.query(kondisi)
    # opsi untuk manggil column -> df['id] atau df.id

    filter = df[df.id == id]

    # if-else condition untuk filter
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="data not found, bruuuuhhhh")
    else: 
        return filter.to_dict(orient='records')

@app.get("/name/{fullname}")
def get_data_name(fullname: str):
    df = pd.read_csv("data.csv")

    filterName = df[df.fullname.str.lower()== fullname.lower()]

    if len(filterName) == 0:
        raise HTTPException(status_code=404, detail="name not found, bruuuuhhhh")
    else: 
        return filterName.to_dict(orient='records')
    
@app.post('/input_data/')
def add_data(update_df:dict):
    df = pd.read_csv('data.csv')
    # define new id for new data
    id = len(df) + 1

    #assign new id to column id in new df named update_df 
    update_df['id'] = id

    # df.append(update_df)
    # return df.to_dict(orient='records')

    new_data = pd.DataFrame([update_df])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save updated DataFrame back to CSV
    df.to_csv('data.csv', index=False)

    return df.to_dict(orient='records')