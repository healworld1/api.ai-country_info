from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint


import os.path
import sys
import json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
CLIENT_ACCESS_TOKEN = '3f578e2210364da29214176ca90623d0'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'

    #print("\n\nYour Input : ",end=" ")
    #request.query = input()

    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)

    print(response_obj["result"]["parameters"]["geo-country"])
    x=response_obj["result"]["parameters"]["geo-country"]

    client = MongoClient('localhost', 27017)
    db = client['apiai']
    collection = db['country_info']

    #pprint.pprint(collection.find_one({"country": "Australia"}))
    #pprint.pprint(collection.find_one({"country": "Belize"}))
    #pprint.pprint(collection.find_one({"country": "China"}))
    #print()
    
    return (collection.find_one({"country": x})["gdb"])


if __name__ == '__main__':
    main()



