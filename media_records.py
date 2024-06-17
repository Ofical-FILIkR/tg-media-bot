from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017"

    client = MongoClient(CONNECTION_STRING)

    dbname = client['records_media']

    return dbname["records"]




def set_record(id, text=None, name=None):
    collection_name = get_database()
    if (text != None):
        item = {
            "id_tg": id,
            "type": "TEXT",
            "content": text,
        }
    else:
        item = {
            "id_tg": id,
            "type": "MEDIA",
            "content": name
        }

    collection_name.insert_one(item)


def get_record(id):
    collection_name = get_database()
    collection = collection_name.find({"id_tg": id})
    for i in collection:
        print(i)
    return collection_name.find({"id_tg": id})


