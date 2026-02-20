from flask import Flask, request
import os
import socket
import time
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.get("/")
def hello():
    worker = socket.gethostname()
    message_received = request.path  # "/" acts as the message for now

    # simulate load / work
    time.sleep(3)

    try:
        conn = get_conn()
        cur = conn.cursor()

        message_received = request.args.get("message")
        if not message_received:
            message_received = "no_message"

        cur.execute(
            "INSERT INTO requests (worker_id, path, status, message_received) VALUES (%s, %s, %s, %s)",
            (worker, request.path, "written", message_received),
        )

        conn.commit()
        cur.close()
        conn.close()

        return f"✅ Written to DB by worker {worker}\n", 200

    except Exception as e:
        logging.exception(f"DB write failed on worker {worker}: {e}")
        return f"❌ Failed to write to DB (worker {worker})\n", 500



@app.get("/double")
def double():
    input_value = request.args.get("number")
    if input_value is None:
        return f"Hello from worker: {socket.gethostname()}\n Example: Provide /double?number=12\n", 200
    
    if not input_value.isdigit():
        return "It is not a number\n", 400
    
    value = int(input_value) * 2
    return f"Worker {socket.gethostname()} doubled the number. New value = {value}\n", 200


@app.get("/busy")
def busy():
    ms = 200
    end = time.time() + (ms / 1000)
    x = 0
    while time.time() < end:
        x += 1
    
    return f"Busy for {ms} ms on {socket.gethostname()}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
