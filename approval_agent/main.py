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

@app.route('/approve', methods=['POST'])
def approve():
    data = request.get_json()
    if data['approved']:
        send_to_queue(data['content'], data['next_queue'])
    else:
        send_to_queue({"content": data['content'], "comments": data['comments']}, data['prev_queue'])
    return {"status": "Review processed"}, 200

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='approval_queue')

    def callback(ch, method, properties, body):
        content = json.loads(body)
        # Here you would typically send this content to a human for approval
        # Simulating approval for demonstration
        approval_data = {"approved": True, "content": content, "next_queue": "next_queue", "prev_queue": "sprint_planning_queue"}
        send_to_queue(approval_data, 'approval_queue')

    channel.basic_consume(queue='approval_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    receive_from_queue()
    app.run(host='0.0.0.0', port=5001)
