from flask import Flask, request
app = Flask("Python-Server")

@app.route("/hello", methods=["GET"])
def function_hello():
    return "Hello World"

app.run(port=5000)