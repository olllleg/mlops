import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer # т.н. преобразователь колонок
from sklearn.linear_model import SGDRegressor
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
from pathlib import Path
import os
from datetime import timedelta
from train_model import train

def download_data():
    #mydata
    df = pd.read_csv('/home/oleg/airflow/dags/International_Education_Costs.csv',  delimiter=',')
    df.to_csv("cost.csv", index = False)
    return df

def clear_data():
    df = pd.read_csv('cost.csv')
    
    cat_columns = ['Country', 'City', 'University', 'Program', 'Level']
    num_columns = ['Duration_Years', 'Tuition_USD', 'Living_Cost_Index', 'Rent_USD','Visa_Fee_USD','Insurance_USD','Exchange_Rate']
    
    
    df = df.dropna()
    df = df.drop_duplicates()
    # Анализ и очистка данных
    # анализ гистограмм
    
    # здравый смысл
    question_duration = df[df["Duration_Years"] > 8]
    df = df.drop(question_duration.index)
    
    # здравый смысл
    question_index = df[df["Living_Cost_Index"] > 100]
    df = df.drop(question_index.index)
    
    # здравый смысл
    question_price = df[df["Tuition_USD"] < 10000]
    df = df.drop(question_price.index)
    
    #анализ гистограмм
    question_visa = df[df['Visa_Fee_USD'] > 1000]
    df = df.drop(question_visa.index)
    
    df = df.reset_index(drop=True)  # обновим индексы в датафрейме DF.
   
    # Порядковое кодирование. Обучение, трансформация и упаковка в df
    
    ordinal = OrdinalEncoder()
    ordinal.fit(df[cat_columns]);
    Ordinal_encoded = ordinal.transform(df[cat_columns])
    df_ordinal = pd.DataFrame(Ordinal_encoded, columns=cat_columns)
    df[cat_columns] = df_ordinal[cat_columns]
    df.to_csv('df_clear.csv')
    return True

dag_cost = DAG(dag_id='train_pipe',
start_date=datetime(2025, 5, 22),
concurrency=4,
schedule_interval=timedelta(minutes=5),
max_active_runs=1,
catchup=False,)

download_task = PythonOperator(python_callable=download_data, task_id ='download_cost',dag = dag_cost)
clear_task = PythonOperator(python_callable=clear_data, task_id = 'clear_cost', dag = dag_cost)
train_task = PythonOperator(python_callable = train, task_id = 'train_cost', dag = dag_cost)
download_task >> clear_task >> train_task
