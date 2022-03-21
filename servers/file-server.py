"""
A Flask file server with CORS support.
"""
import sys
import flask
from flask import Flask, send_from_directory, request
from flask_cors import CORS, cross_origin

app = Flask(__name__,
            static_url_path='', 
            static_folder='./',
            template_folder='./')

app.secret_key = "this is only for testing"
CORS(app, send_wildcard=True, expose_headers=[])
count = 0

@app.after_request
def process(response):
    global count
    print('\n============== Request Count:' + str(count) + ' ==============')
    count = count + 1
    # log the request
    print(request.method + ' ' + request.full_path)
    for h in request.headers:
        print(h[0] + ': ' + h[1])
    print('\n' + request.stream.read().decode(), file=sys.stderr)
    # return original response
    return response

@app.after_request
def apply_caching(response):
    response.headers["Custom-Header"] = "Custom-Value"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
    # change the port to something above 1024 if you don't want to run as root.
