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
REQUIREMENTS_QUEUE = os.getenv('REQUIREMENTS_QUEUE', 'requirements_queue')

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

@app.route('/gather', methods=['POST'])
def gather_requirements():
    """Endpoint to gather requirements and send them to the analysis queue."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input, JSON required"}), 400

        send_to_queue(data, REQUIREMENTS_QUEUE)
        return jsonify({"status": "Requirements received and sent to the analysis queue"}), 200
    except Exception as e:
        logger.error(f"Error in gathering requirements: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
