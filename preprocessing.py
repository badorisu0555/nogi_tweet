import pandas as pd
from sentence_transformers import SentenceTransformer
import json
from bertopic import BERTopic
from hdbscan import HDBSCAN
import re

from pprint import pprint
import emoji

import os
from dotenv import load_dotenv

def remove_emoji(text):
    return emoji.replace_emoji(text,replace='')

def open_json(json_open):
    id = []
    text = []
    viewCount = []
    likeCount = []
    url = []

    for i in range(len(json_open)):
        id.append(json_open[i]["id"])
        text.append(json_open[i]["text"])
        viewCount.append(json_open[i]["viewCount"])
        likeCount.append(json_open[i]["likeCount"])
        url.append(json_open[i]["url"])

    df = pd.DataFrame({
        "id":id,
        "text":text,
        "viewCount":viewCount,
        "likeCount":likeCount,
        "url":url})
    
    return df

def remove_urls(df):
    df["text"] = df["text"].str.replace("\n","")
    pattern = r'https?://[^\s]+'
    df["text"] = df["text"].apply(lambda x:re.sub(pattern,"",x))
    return df

json_open = open("nogizaka_tweets.json","r",encoding="utf-8")
json_open = json.load(json_open)
df = open_json(json_open)
df = remove_urls(df)
df["text"] = df["text"].apply(lambda x: remove_emoji(x))

df_json = df.to_json(orient='records',force_ascii=False)
#pprint(df_json)