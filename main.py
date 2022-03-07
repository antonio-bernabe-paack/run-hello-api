import os
from flask import Flask, request
import json

# create a Flask instance
app = Flask(__name__)

# a simple description of the API written in html.
# Flask can print and return raw text to the browser. 
# This enables html, json, etc. 

description =   """
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>  
                    <h3>A simple API using Flask</h3>
                    <p> Usage: http://FQDN/api?value=2</p>
                </body>
                """
				
# Routes refer to url'
# our root url '/' will show our html description
@app.route('/', methods=['GET'])
def hello_world():
    # return a html format string that is rendered in the browser
	return description

# our '/api' url
# requires user integer argument: value
# returns error message if wrong arguments are passed.
@app.route('/api', methods=['GET'])
def square():
    if not all(k in request.args for k in (["value"])):
        supplied_parameters = f"{[k for k in request.args]}"
        return json.dumps({"Required parameters" : 'value', "Supplied parameters" : supplied_parameters}), 400
    else:
        # assign and cast variable to int
        value = int(request.args['value'])
        # or use the built in get method and assign a type
        # http://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.MultiDict.get
        value = request.args.get('value', type=int)
        secret = os.environ.get("RUN_HELLO_API_SECRET")
        config = os.environ.get("RUN_HELLO_API_CONFIG")
        return json.dumps({"Value Squared" : value**2, "secret" : secret, "config" : config})

if __name__ == "__main__":
	# for debugging locally
	# app.run(debug=True, host='0.0.0.0',port=5000)
	
	# for production
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
