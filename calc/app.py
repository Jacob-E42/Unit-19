"""Basic app that performs four functions on query strings """
from flask import Flask, request 
from operations import add, sub, mult, div
app = Flask(__name__)

@app.route("/add")
def addition():
    a = int(request.args["a"])
    b = int(request.args["b"])
    result = add(a, b)
    return str(result)

@app.route("/sub")
def subtract():
    a = int(request.args["a"])
    b = int(request.args["b"])
    return str(sub(a, b))

@app.route("/mult")
def multiply():
    a = int(request.args["a"])
    b = int(request.args["b"])
    return str(mult(a, b))

@app.route("/div")
def divide():
    a = int(request.args["a"])
    b = int(request.args["b"])
    return str(div(a, b))
