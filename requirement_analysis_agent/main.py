from dotenv import load_dotenv
import os
import pika
import json
import spacy
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
REQUIREMENTS_QUEUE = os.getenv('REQUIREMENTS_QUEUE', 'requirements_queue')
ANALYSIS_QUEUE = os.getenv('ANALYSIS_QUEUE', 'analysis_queue')

def analyze_requirements(requirements):
    """Analyze the given requirements using SpaCy and perform validation."""
    logger.debug(f"Analyzing requirements: {requirements}")
    doc = nlp(requirements["text"])
    analysis = [(ent.text, ent.label_) for ent in doc.ents]
    return {"status": "valid", "analysis": analysis}

def receive_from_queue():
    """Receive messages from the requirements queue and analyze them."""
    try:
        logger.debug(f"Connecting to RabbitMQ at {RABBITMQ_HOST}")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        # Ensure the queue declaration is consistent
        channel.queue_declare(queue=REQUIREMENTS_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            requirements = json.loads(body)
            logger.info(f"Received requirements: {requirements}")
            analysis = analyze_requirements(requirements)
            if analysis["status"] == "valid":
                send_to_next_queue(analysis, ANALYSIS_QUEUE)
            else:
                send_to_next_queue(analysis, REQUIREMENTS_QUEUE)

        channel.basic_consume(queue=REQUIREMENTS_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the requirements queue")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Failed to receive from queue: {e}")
        raise

def send_to_next_queue(message, queue_name):
    """Send a message to the specified RabbitMQ queue."""
    try:
        logger.debug(f"Connecting to RabbitMQ at {RABBITMQ_HOST}")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        # Ensure the queue declaration is consistent
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        logger.info(f"Message sent to queue {queue_name}")
    except Exception as e:
        logger.error(f"Failed to send message to queue {queue_name}: {e}")
        raise

if __name__ == "__main__":
    receive_from_queue()