from dotenv import load_dotenv
import os
import pika
import json
from flask import Flask, request, jsonify
import logging
import tempfile
import shutil
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
REQUIREMENTS_QUEUE = os.getenv('REQUIREMENTS_QUEUE', 'requirements_queue')

# Temporary storage for user inputs
temp_dir = tempfile.mkdtemp()

requirements = {
    "documents": [],
    "images": [],
    "text": [],
    "code": [],
    "links": []
}

def save_file(file, file_type):
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    requirements[file_type].append(file_path)
    logger.info(f"Saved {file_type} file: {file_path}")

@app.route('/api/gather', methods=['POST'])
def gather_requirements():
    """Endpoint to gather requirements from user input."""
    try:
        if 'files' in request.files:
            for file in request.files.getlist('files'):
                file_type = request.form.get('type', 'text')
                save_file(file, file_type)
        elif 'links' in request.json:
            requirements["links"].extend(request.json['links'])
            logger.info(f"Added links: {request.json['links']}")
        elif 'text' in request.json:
            requirements["text"].append(request.json['text'])
            logger.info(f"Added text: {request.json['text']}")
        else:
            return jsonify({"error": "Invalid input, files or JSON required"}), 400

        return jsonify({"status": "Requirements received. Add more or finalize."}), 200
    except Exception as e:
        logger.error(f"Error in gathering requirements: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/finalize', methods=['POST'])
def finalize_requirements():
    """Endpoint to finalize and send the collected requirements to the analysis queue."""
    try:
        send_to_queue(requirements, REQUIREMENTS_QUEUE)
        shutil.rmtree(temp_dir)  # Clean up temporary directory
        return jsonify({"status": "Requirements finalized and sent to the analysis queue"}), 200
    except Exception as e:
        logger.error(f"Error in finalizing requirements: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Endpoint to fetch logs."""
    # Implement logic to fetch logs
    logs = ["Log entry 1", "Log entry 2", "Log entry 3"]  # Replace with actual log fetching logic
    return jsonify(logs)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
