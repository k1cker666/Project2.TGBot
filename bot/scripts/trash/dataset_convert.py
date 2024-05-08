import time
import pandas as pd
from googletrans import Translator

# pip install googletrans==4.0.0-rc1
# pip install httpx==0.13

def fetch_word_and_level():
    cols = pd.read_csv('bot/scripts/trash/oxford-5k.csv', nrows=0).columns
    cols = cols[cols.str.contains('(?:^word$|level)')].tolist()
    df = pd.read_csv(filepath_or_buffer='bot/scripts/trash/oxford-5k.csv', usecols=cols)
    df.loc[df['level'] == 'a1', 'level'] = 'A1'
    df.loc[df['level'] == 'a2', 'level'] = 'A1'
    df.loc[df['level'] == 'b1', 'level'] = 'A2'
    df.loc[df['level'] == 'b2', 'level'] = 'A1'
    df.loc[df['level'] == 'c1', 'level'] = 'A3'
    df.drop_duplicates(subset=['word']).to_csv('bot/scripts/trash/res.csv', sep=',', header=True)

def get_inserts_sql():
    translator = Translator()
    df = pd.read_csv('bot/scripts/trash/res.csv', sep=',', header=0)
    dataset = df.to_dict('split')['data']
    with open('bot/dataset/insert.sql', 'a') as fl:
        id = 929
        for data in dataset:
            trans = translator.translate(data[1], dest='ru', src='en')
            string = "insert into words (word_id, language, level, word) " + \
                f"values ({id}, 'en', '{data[2]}', '{data[1]}');\n" + \
                "insert into words (word_id, language, level, word) " + \
                f"values ({id}, 'ru', '{data[2]}', '{trans.text.lower()}');\n"
            fl.write(string)
            id += 1
            time.sleep(0.4)
            
if __name__ == "__main__":
    get_inserts_sql()