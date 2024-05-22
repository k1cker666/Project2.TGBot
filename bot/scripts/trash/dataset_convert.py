import time

import pandas as pd
from googletrans import Translator


# pip install googletrans==4.0.0-rc1
# pip install httpx==0.13 0.26.0


def fetch_word_and_level():
    cols = pd.read_csv("bot/scripts/trash/oxford-5k.csv", nrows=0).columns
    cols = cols[cols.str.contains("(?:^word$|level)")].tolist()
    df = pd.read_csv(
        filepath_or_buffer="bot/scripts/trash/oxford-5k.csv", usecols=cols
    )
    df.loc[df["level"] == "a1", "level"] = "A1"
    df.loc[df["level"] == "a2", "level"] = "A1"
    df.loc[df["level"] == "b1", "level"] = "A2"
    df.loc[df["level"] == "b2", "level"] = "A1"
    df.loc[df["level"] == "c1", "level"] = "A3"
    df.drop_duplicates(subset=["word"]).to_csv(
        "bot/scripts/trash/res.csv", sep=",", header=True
    )


def add_translate():
    translator = Translator()
    translations = []
    df = pd.read_csv("bot/scripts/trash/res.csv", sep=",", header=0)
    count = 0
    for word in df["word"]:
        translated_word = translator.translate(word, dest="ru", src="en")
        translations.append(translated_word.text.lower())
        count += 1
        if count % 10 == 0:
            print(f"{count}/4953 ready")
        time.sleep(0.4)
    df["word_translate"] = translations
    df.to_csv(
        "bot/scripts/trash/res_with_translate.csv",
        sep=",",
        index=False,
        header=True,
    )


def drop_translate_dublicates():
    df = pd.read_csv(
        "bot/scripts/trash/res_with_translate.csv", sep=",", header=0
    )
    df.drop_duplicates(subset=["word_translate"]).to_csv(
        "bot/scripts/trash/res_trans_no_dubl.csv",
        sep=",",
        header=True,
        index=False,
    )


def find_dublicates():
    df_full = pd.read_csv("res_with_translate.csv")
    df_unique = pd.read_csv("res_trans_no_dubl.csv")
    df_duplicates = df_full.merge(
        df_unique, on="word", how="outer", indicator=True
    )
    df_duplicates = df_duplicates[df_duplicates["_merge"] == "left_only"].drop(
        columns="_merge"
    )
    df_duplicates.to_csv("duplicates_file.csv", index=False)


def get_inserts_sql():
    df = pd.read_csv(
        "bot/scripts/trash/res_trans_no_dubl.csv", sep=",", header=0
    )
    dataset = df.to_dict("split")["data"]
    with open("bot/scripts/sql/insert.sql", "w") as fl:
        id = 1
        for data in dataset:
            string = (
                "insert into words (word_id, language, level, word) "
                + f"values ({id}, 'en', '{data[2]}', '{data[1]}');\n"
                + "insert into words (word_id, language, level, word) "
                + f"values ({id}, 'ru', '{data[2]}', '{data[3]}');\n"
            )
            fl.write(string)
            id += 1


if __name__ == "__main__":
    get_inserts_sql()
