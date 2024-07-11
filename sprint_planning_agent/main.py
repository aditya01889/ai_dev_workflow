from dotenv import load_dotenv
import os
import pika
import json
import random
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
ANALYSIS_QUEUE = os.getenv('ANALYSIS_QUEUE', 'analysis_queue')
APPROVAL_QUEUE = os.getenv('APPROVAL_QUEUE', 'approval_queue')
FRONTEND_COMPONENT_QUEUE = os.getenv('FRONTEND_COMPONENT_QUEUE', 'frontend_component_queue')
BACKEND_MICROSERVICE_QUEUE = os.getenv('BACKEND_MICROSERVICE_QUEUE', 'backend_microservice_queue')
DATABASE_SCHEMA_QUEUE = os.getenv('DATABASE_SCHEMA_QUEUE', 'database_schema_queue')
API_GATEWAY_QUEUE = os.getenv('API_GATEWAY_QUEUE', 'api_gateway_queue')

def estimate_effort(task):
    """Estimate effort for a given task."""
    effort = random.randint(1, 10)
    logger.info(f"Estimated effort for task '{task}': {effort}")
    return effort

def create_user_stories(analysis):
    """Create user stories, estimate effort, and allocate tasks based on the analysis."""
    tasks = {
        "Build frontend": FRONTEND_COMPONENT_QUEUE,
        "Create backend API": BACKEND_MICROSERVICE_QUEUE,
        "Design database schema": DATABASE_SCHEMA_QUEUE,
        "Create API gateway": API_GATEWAY_QUEUE
    }
    
    user_stories = []
    for task, queue in tasks.items():
        story = {
            "task": task,
            "effort": estimate_effort(task),
            "assigned_to": queue
        }
        user_stories.append(story)
    
    logger.info(f"Created user stories with estimates: {user_stories}")
    return user_stories

def receive_from_queue():
    """Receive messages from the analysis queue and create user stories."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=ANALYSIS_QUEUE)

        def callback(ch, method, properties, body):
            analysis = json.loads(body)
            logger.info(f"Received analysis: {analysis}")
            user_stories = create_user_stories(analysis)
            send_to_next_queue({"user_stories": user_stories}, APPROVAL_QUEUE)

        channel.basic_consume(queue=ANALYSIS_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the analysis queue")
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
