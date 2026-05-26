import requests
import pandas as pd 
import io
import sqlite3

def extract(url):
    res = requests.get(url)
    res.raise_for_status()

    df = pd.read_csv(io.StringIO(res.text))
    return df

def transform(df:pd.DataFrame):
    #headers
    df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')
    #rows
    string_cols = ['patient_name','gender','medication','condition']
    df[string_cols] = df[string_cols].apply(lambda x:x.str.lower().str.strip().str.replace(' ','_'))
    #duplicates
    df.drop_duplicates(keep='first',inplace=True)
    #removing
    df.dropna(subset=['condition'],inplace=True)
    #fixing rows
    #cleaning age
    df['age'] = df['age'].replace({'forty': '40', 'thirty': '30', 'twenty': '20'})
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['age'] = df['age'].fillna(df['age'].median())
    df['age'] = df['age'].astype(float)
    #clean cholesterol
    df['cholesterol'] = pd.to_numeric(df['cholesterol'],errors='coerce')
    df['cholesterol'] = df['cholesterol'].fillna(df['cholesterol'].median())
    df['email'] = df['email'].fillna('unknown')
    df['phone_number'] = df['phone_number'].fillna('not_provided')
    df['blood_pressure'] = df['blood_pressure'].fillna('unkown')
    #fixing date
    df['visit_date'] = pd.to_datetime(df['visit_date'],format="mixed",errors='coerce') 
    return df

def validate(df:pd.DataFrame):
    checks = {
        'no null condiions' : df['condition'].isna().sum() == 0,
        'valid gender': df['gender'].isin(['male','female','other']).all(),
        'positive age' : (df['age']>0).all(),
        'positive cholesterol': (df['cholesterol']>0).all()
    }

    passed = True
    for check,result in checks.items():
        if not result:
            print(f"x{check}")
            passed = False
    return passed

def load(df:pd.DataFrame,db_path:str):
    conn = sqlite3.connect(db_path)
    df.to_sql('healthcare',conn,if_exists='replace',index=False)
    conn.close()
    print('loaded')


if __name__ == "__main__":
    pd.set_option('display.max_columns',None)
    pd.set_option('display.width',900)
    url_link = "https://raw.githubusercontent.com/eyowhite/Messy-dataset/refs/heads/main/healthcare_messy_data.csv"
    df = extract(url_link)
    df = transform(df)
    if validate(df):
        load(df,'healthcare.db')
    else:
        print('failed')
