import pymongo
import json
import math
from pymongo import MongoClient

def search(query):
    query_tokens = query.split()

    client = pymongo.MongoClient("mongodb+srv://chanman:<password>@cluster0.ksokk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE")
    db = client["mydatabase"]
    db_collection = db["mycollection"]
    
    #open total_tokens file
    total_tokens =  open("total_tokens.json",'r')
    num_of_tokens = json.loads(total_tokens.read()) 

    #bookkeeping file gets the link relative to the local path
    links = open("WEBPAGES_RAW/bookkeeping.json","r")
    doc_links = json.loads(links.read())

    result_paths = {} #{path : tf-idf} ex. {0/0 : 0.38}

    #iterate through each word in the query
    for word in query_tokens:

        #search db for the token
        listing = db_collection.find({"token": word}, {"_id": 0, "token": 0})[0]

        doc_paths = {} #{ path : token_freq } ex. { "23/376" : 19 }

        num_docs = [] #has token count of files that have the token in it 
        #also used to get the number of docs with that token

       
        listing_len = len(listing)

        #if no results, go next
        if (listing_len == 0):
            continue

        #idf : inverse document frequency
        idf = math.log(len(num_of_tokens) / listing_len)

        #go through search query results and get the doc-id and the term frequency for that document
        for x in listing.values():
            temp_doc = x['document']
            temp_freq = x['frequency']
            doc_paths[temp_doc] = temp_freq
            num_docs.append(num_of_tokens[temp_doc]) #num_of_tokens correlates the file path to the number of tokens the file has
        

        idx = 0

        #calculate the tf-idf 
        for doc, freq in doc_paths.items():
            tf = freq / num_docs[idx]
            tf_idf = tf * idf
            idx += 1

            #for multiple queries
            #if there is a matching path, add to  the tf-idf else, make new entry
            if (doc in result_paths):
                result_paths[doc] = result_paths[doc] + tf_idf
            else:
                result_paths[doc] = tf_idf
        
    #sort by tf-idf highest-lowest
    sorted_list = sorted(result_paths.items(), key=lambda x: -x[1])
    result = []

    for doc in sorted_list:
        a = doc[0].split('\\')
        b = a[0] + '/' + a[1]
        result.append(doc_links[b]) #doc_links correlates the file path to a url

    return result

