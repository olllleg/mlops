import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

def download_data():
    #mydata
    df = pd.read_csv('/var/lib/jenkins/workspace/download/mlops/lab3/International_Education_Costs.csv',  delimiter=',')
    df.to_csv("cost.csv", index = False)
    return df

def clear_data(path2df):
    df = pd.read_csv(path2df)
    
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
    
    df = df.reset_index(drop=True)  # обновим индексы в датафрейме DF. если бы мы прописали drop = False, то была бы еще одна колонка - старые индексы
   
    # Порядковое кодирование. Обучение, трансформация и упаковка в df
    
    ordinal = OrdinalEncoder()
    ordinal.fit(df[cat_columns]);
    Ordinal_encoded = ordinal.transform(df[cat_columns])
    df_ordinal = pd.DataFrame(Ordinal_encoded, columns=cat_columns)
    df[cat_columns] = df_ordinal[cat_columns]
    df.to_csv('df_clear.csv')
    return True

download_data()
clear_data("cost_csv.csv")
