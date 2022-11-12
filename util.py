import requests
import json
import pandas as pd

import ipdb

STATS = ['attack', 'health', 'defense', 'effectiveness', 'effect resistance', 'critical hit chance', 'critical hit damage', 'speed']

def fetch_ocr(url: str) -> str:
    print(f'Making api call with url: {url}')
    payload = {
        'url': url,
        'apikey': 'K82384577388957',
        'OCREngine': 2,
    }
    res = requests.post(
            'https://api.ocr.space/parse/image',
            data=payload,
        )
    res_json = json.loads(res.content.decode()) 
    raw_text = res_json['ParsedResults'][0]['ParsedText']
    print(f'Received: {raw_text}')
    return raw_text
        
def transform_raw_text(raw_text: str) -> pd.DataFrame:
    tokens = raw_text.lower().split('\n')
    while tokens[0] not in STATS:
        tokens = tokens[1:]
    tokens = tokens[2:]
    stats, nums = tokens[:len(tokens)//2],tokens[len(tokens)//2:]
    gear_df = pd.DataFrame({'stat':stats,'values':nums})
    gear_df['stat_type'] = gear_df.apply(lambda row: '%' if row['values'][-1]=='%' else 'flat', axis=1)
    gear_df['values'] = gear_df['values'].str.rstrip("%").astype(float)
    return gear_df

def calculate_gear_score(gear_df: pd.DataFrame) -> str:
    gear_score_df = pd.read_csv('res/gear_score.csv')
    gear_score_df['multiplier'] = gear_score_df['multiplier'].astype(float)
    calc_df = gear_df.merge(gear_score_df,on=['stat','stat_type'])
    calc_df['score'] = calc_df.apply(lambda row: row['values']*row['multiplier'],axis=1)
    score = calc_df['score'].sum()
    return f'Your gear score is: {score}'

def call_gear_score(url: str) -> str:
    try:
        raw_text = fetch_ocr(url)
        gear_df = transform_raw_text(raw_text)
        return calculate_gear_score(gear_df)
    except Exception as e:
        print(f"Error: {e}")
        return "Error: could not successfully calculate gear score"