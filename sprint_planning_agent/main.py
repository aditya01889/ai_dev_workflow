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

def estimate_effort(task):
    """Estimate effort for a given task."""
    effort = random.randint(1, 10)
    logger.info(f"Estimated effort for task '{task}': {effort}")
    return effort

def create_user_stories(analysis):
    """Create user stories and estimate effort based on the analysis."""
    tasks = ["Build frontend", "Create backend API", "Design database schema"]
    task_estimates = {task: estimate_effort(task) for task in tasks}
    logger.info(f"Created user stories with estimates: {task_estimates}")
    return task_estimates

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
            send_to_next_queue(user_stories, APPROVAL_QUEUE)

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
