import os
import parse
from collections import defaultdict
import pymongo
import json

#connect to db
client = pymongo.MongoClient("mongodb+srv://chanman:<password>@cluster0.ksokk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE")
db = client["mydatabase"]
db_collection = db["mycollection"]

#initialize variables 
unique_id = 0
id_num = "id_num"
operations = []
token_freq = {}

#create hashed index
db_collection.create_index([("token",pymongo.HASHED)])

#iterate through each file
for subdir, dirs, files in os.walk("WEBPAGES_RAW"):
    for f in files:

        # avoid files with extensions 
        if f.endswith('.json') or f.endswith('.tsv') or f.endswith('.DS_Store'):
            continue

        #HTML files will now get parsed
        path_to_file = os.path.join(subdir,f)

        #parse file
        data_of_file = parse.parse(path_to_file)

        #changes ex. WEBPAGES_RAW/30/244 to 30/244
        num_path = path_to_file[13:]
        token_freq[num_path] = 0
        print(num_path)
        
        #go through each {token : freq} for a file 
        for token, freq in data_of_file.items():

            #adds to total token_freq of that file
            token_freq[num_path] += (freq)
            
            #makes a unique id
            id_num += str(unique_id)

            #use upsert to add new or update token with a new listing with a given document and the token's frequency
            operations.append(pymongo.UpdateOne({"token":token}, {"$set": {id_num: {"document": num_path, "frequency": freq}}}, upsert=True))
            id_num = "id_num"
            unique_id += 1
            
    # after each file of 500, write to db
    if operations != []:
        db_collection.bulk_write(operations)
        operations = []
    
#writes word count of each and every file to calc tf-idf
file = open("total_tokens.json","w")
json.dump(token_freq, file)
file.close()

