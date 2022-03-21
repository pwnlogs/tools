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
    print('\n============== Request Count:' + str(count) + ' ==============', flush=True)
    count = count + 1
    # log the request
    print(request.method + ' ' + request.full_path, flush=True)
    for h in request.headers:
        print(h[0] + ': ' + h[1], flush=True)
    print('\n' + request.stream.read().decode(), file=sys.stderr, flush=True)
    # return original response
    return response

@app.after_request
def apply_caching(response):
    response.headers["Custom-Header"] = "Custom-Value"
    return response


if __name__ == "__main__":
    context = ('example.local.crt', 'example.local.priv-key.pem')
    app.run(host='example.local', debug=True, ssl_context=context, port=443)
