from dotenv import load_dotenv
import os
import pika
import json
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

def send_to_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

@app.route('/gather', methods=['POST'])
def gather_requirements():
    data = request.get_json()
    send_to_queue(data, 'requirements_queue')
    return {"status": "Requirements received and sent to the analysis queue"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
