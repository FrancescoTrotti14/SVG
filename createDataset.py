from pymongo import MongoClient
import pandas as pd

df_project = pd.DataFrame()
client = MongoClient('localhost', 27017)
db = client.tesi
collection = db.issue

key1 = "html_url"
key2 = "repository_url"

result = collection.find({}, {"_id" : 0, "html_url" : 1, "repository_url": 1}, batch_size=20)

def create_dataset(result):
    for user in result:
        if (key1 in user and key2 in user):
            df_project = df_project.append({
                'html_url': user.__getitem__("html_url"),
                'repository_url': user.__getitem__("repository_url")
            }, ignore_index = True)
    df_project.to_csv('Dataset/issues.csv', sep=',', encoding='utf-8', index=False)