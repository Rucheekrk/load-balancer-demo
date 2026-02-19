from flask import Flask, request
import socket

app = Flask(__name__)

@app.get("/")
def hello():
    print ("Hello from worker: {socket.gethostname()}\n")
    input_value = request.args.get("number")
    if input_value is None:
        return f"Hello from worker: {socket.gethostname()}\n Example: Provide ?number=12\n", 200
    
    if not input_value.isdigit():
        return "It is not a number\n", 400
    
    value = int(input_value) * 2
    return f"Worker {socket.gethostname()} doubled the number. New value = {value}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
