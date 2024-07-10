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

def analyze_requirements(requirements):
    """
    Analyze the given requirements using SpaCy and perform validation.
    :param requirements: dict containing the requirements
    :return: dict with validation status and analysis or error message
    """
    # Check for presence of required fields
    required_fields = ["text", "project_id", "author"]
    for field in required_fields:
        if field not in requirements:
            return {"status": "invalid", "message": f"Missing required field: {field}"}
    
    # Validate field data types
    if not isinstance(requirements["text"], str):
        return {"status": "invalid", "message": "Field 'text' must be a string"}
    if not isinstance(requirements["project_id"], int):
        return {"status": "invalid", "message": "Field 'project_id' must be an integer"}
    if not isinstance(requirements["author"], str):
        return {"status": "invalid", "message": "Field 'author' must be a string"}

    # Validate content
    if len(requirements["text"]) < 20:
        return {"status": "invalid", "message": "Field 'text' must be at least 20 characters long"}

    # Semantic validation using SpaCy
    doc = nlp(requirements["text"])
    if len(doc.ents) == 0:
        return {"status": "invalid", "message": "Field 'text' must contain at least one named entity"}

    # Business Rule: Ensure text contains certain mandatory keywords
    mandatory_keywords = ["deadline", "requirement", "feature"]
    if not any(keyword in requirements["text"].lower() for keyword in mandatory_keywords):
        return {"status": "invalid", "message": f"Field 'text' must contain at least one of the mandatory keywords: {mandatory_keywords}"}

    # Business Rule: Validate dates mentioned in the text (if any)
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    # Example check: Ensure dates are within the next year
    if dates:
        from datetime import datetime, timedelta
        one_year_later = datetime.now() + timedelta(days=365)
        for date in dates:
            try:
                parsed_date = datetime.strptime(date, "%B %d, %Y")  # Adjust the date format as per your requirements
                if parsed_date > one_year_later:
                    return {"status": "invalid", "message": f"Date {date} is too far in the future"}
            except ValueError:
                return {"status": "invalid", "message": f"Date {date} is not in a valid format"}

    # Business Rule: Validate project_id and author (mocked for example purposes)
    valid_project_ids = [101, 102, 103]  # Example project IDs
    valid_authors = ["alice", "bob", "carol"]  # Example authors
    if requirements["project_id"] not in valid_project_ids:
        return {"status": "invalid", "message": "Invalid project_id"}
    if requirements["author"].lower() not in valid_authors:
        return {"status": "invalid", "message": "Invalid author"}

    # If all validations pass, return the analysis
    analysis = [(ent.text, ent.label_) for ent in doc.ents]
    return {"status": "valid", "analysis": analysis}

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
