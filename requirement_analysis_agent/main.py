from dotenv import load_dotenv
import os
import pika
import json
import spacy
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
REQUIREMENTS_QUEUE = os.getenv('REQUIREMENTS_QUEUE', 'requirements_queue')
ANALYSIS_QUEUE = os.getenv('ANALYSIS_QUEUE', 'analysis_queue')
REQUIREMENT_GATHERING_QUEUE = os.getenv('REQUIREMENT_GATHERING_QUEUE', 'requirement_gathering_queue')

def analyze_requirements(requirements):
    """
    Analyze the given requirements using SpaCy and perform validation.
    :param requirements: dict containing the requirements
    :return: dict with validation status and analysis or error message
    """
    schema = requirements.get("schema", {})
    data = requirements.get("data", {})

    # Validate data against the schema
    for field, rules in schema.items():
        if field not in data:
            return {"status": "invalid", "message": f"Missing required field: {field}", "field": field}
        if "type" in rules and not isinstance(data[field], rules["type"]):
            return {"status": "invalid", "message": f"Field '{field}' must be of type {rules['type'].__name__}", "field": field}
        if "min_length" in rules and len(data[field]) < rules["min_length"]:
            return {"status": "invalid", "message": f"Field '{field}' must be at least {rules['min_length']} characters long", "field": field}

    # Perform content analysis using SpaCy
    if "text" in data:
        doc = nlp(data["text"])
        if len(doc.ents) == 0:
            return {"status": "invalid", "message": "Field 'text' must contain at least one named entity", "field": "text"}
        data["entities"] = [(ent.text, ent.label_) for ent in doc.ents]

    return {"status": "valid", "data": data}

def receive_from_queue():
    """Receive messages from the requirements queue and analyze them."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=REQUIREMENTS_QUEUE)

        def callback(ch, method, properties, body):
            requirements = json.loads(body)
            logger.info(f"Received requirements: {requirements}")
            analysis = analyze_requirements(requirements)
            if analysis["status"] == "valid":
                send_to_next_queue(analysis, ANALYSIS_QUEUE)
            else:
                logger.info(f"Validation failed: {analysis['message']}")
                send_to_next_queue(analysis, REQUIREMENT_GATHERING_QUEUE)

        channel.basic_consume(queue=REQUIREMENTS_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the requirements queue")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Failed to receive from queue: {e}")
        raise

def send_to_next_queue(message, queue_name):
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
    receive_from_queue()
