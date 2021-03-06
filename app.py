#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "country_info":
        return {}


    #get country
    parameters = req.get("result").get("parameters")
    country = parameters.get("geo-country")
    topic = parameters.get("topic")

    res = makeWebhookResult(country,topic)
    return res

def makeWebhookResult(country,topic):


    if topic == "GDP":
        json_file = open("gdp.json")
        topic = "GDP"
    elif topic == "population":
        json_file = open("population.json")
        topic = "population"
    
    value = 0
    for line in json_file:
        if json.loads(line)["country"] == country:
            value = json.loads(line)[topic]
            break
    
    if value ==0:
        return {}
    
    speech = "The " + topic +" of " + country + " is " + value + " in 2015. Anything else?"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-country-info"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
