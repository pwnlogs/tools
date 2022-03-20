"""
A Flask file server with CORS support.
"""
import sys
import flask
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__,
            static_url_path='', 
            static_folder='./',
            template_folder='./')

app.secret_key = "this is only for testing"
CORS(app, send_wildcard=True, expose_headers=[])


@app.after_request
def apply_caching(response):
    response.headers["Custom-Header"] = "Custom-Value"
    return response


if __name__ == "__main__":
    context = ('example.local.crt', 'example.local.priv-key.pem')
    app.run(host='example.local', debug=True, ssl_context=context, port=443)
