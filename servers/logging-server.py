"""
A Flask server that prints the requests received.
The server will print the raw request on console and respond 200 OK.
This is used for testing issues such as SSRF.

Note: The server allows CORS.
"""
import sys
import flask
from flask import Flask, flash, request, redirect, render_template, Response
from flask.wrappers import Request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.routing import Rule


app = Flask(__name__)
app.secret_key = "this is only for testing"
CORS(app)
count = 1


def process(req):
    global count
    print('\n============== Request Count:' + str(count) + ' ==============')
    count = count + 1

    # log the request
    print(req.method + ' ' + req.full_path)
    for h in req.headers:
        print(h[0] + ': ' + h[1])
    print('\n' + req.stream.read().decode(), file=sys.stderr)

    # create the response
    resp = flask.Response('logged')
    # resp.headers["header1"] = "value1" # add if you need
    return resp
    

@app.route('/', methods=['GET','POST'])
@cross_origin()
def index():
    return process(request)


# catch all paths here
@app.route('/<path:path>', methods=['GET','POST'])
@cross_origin()
def any(path):
    return process(request)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')  # change the port to something above 1024 if you don't want to run as root.
