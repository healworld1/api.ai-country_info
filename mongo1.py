#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys
from pymongo import MongoClient
import pprint

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=2))

    res = processRequest(req)

    res = json.dumps(res, indent=2)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "country_info":
        return {}


    #data
    result = req.get("result") 
    parameters = result.get("parameters") 
    country = parameters.get("geo-country")

    res = makeWebhookResult(country)
    return res

def makeWebhookResult(country):

    #mongo
    client = MongoClient('localhost', 27017)
    db = client['apiai']
    collection = db['country_info']
    
    speech = (collection.find_one({"country": country})["gdp"])
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        "source": "heroku-apiai-country-info"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
