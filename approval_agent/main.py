from dotenv import load_dotenv
import os
import pika
import json
from flask import Flask, request, jsonify
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
APPROVAL_QUEUE = os.getenv('APPROVAL_QUEUE', 'approval_queue')

def send_to_queue(message, queue_name):
    """Send a message to the specified RabbitMQ queue."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        connection.close()
        logger.info(f"Message sent to queue {queue_name}")
    except Exception as e:
        logger.error(f"Failed to send message to queue {queue_name}: {e}")
        raise

@app.route('/approve', methods=['POST'])
def approve():
    """Endpoint to process approval or rejection of content."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON required"}), 400

    if 'approved' not in data or 'content' not in data or 'next_queue' not in data or 'prev_queue' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if data['approved']:
        send_to_queue(data['content'], data['next_queue'])
    else:
        if 'comments' not in data:
            return jsonify({"error": "Missing comments for rejection"}), 400
        send_to_queue({"content": data['content'], "comments": data['comments']}, data['prev_queue'])

    return jsonify({"status": "Review processed"}), 200

def receive_from_queue():
    """Receive messages from the approval queue and process them."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=APPROVAL_QUEUE)

        def callback(ch, method, properties, body):
            content = json.loads(body)
            logger.info(f"Received content for approval: {content}")
            # Here you would typically send this content to a human for approval
            # Simulating approval for demonstration
            approval_data = {
                "approved": True, 
                "content": content, 
                "next_queue": "next_queue", 
                "prev_queue": "sprint_planning_queue"
            }
            send_to_queue(approval_data, APPROVAL_QUEUE)

        channel.basic_consume(queue=APPROVAL_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the approval queue")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Failed to receive from queue: {e}")
        raise

if __name__ == "__main__":
    receive_from_queue()
    app.run(host='0.0.0.0', port=5001)
