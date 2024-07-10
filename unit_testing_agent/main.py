from dotenv import load_dotenv
import os
import pika
import json
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
APPROVAL_QUEUE = os.getenv('APPROVAL_QUEUE', 'approval_queue')
UNIT_TEST_QUEUE = os.getenv('UNIT_TEST_QUEUE', 'unit_test_queue')

def generate_unit_tests(task_description, code_snippet):
    """Generate unit tests based on the provided code snippet and task description."""
    tests = f"""
import pytest

def test_function():
    result = {code_snippet}
    assert result == expected_output

if __name__ == "__main__":
    pytest.main()
    """
    logger.info(f"Generated unit tests for task '{task_description}': {tests}")
    return tests

def receive_from_queue():
    """Receive messages from the approval queue and generate unit tests."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=APPROVAL_QUEUE)

        def callback(ch, method, properties, body):
            user_stories = json.loads(body)
            logger.info(f"Received user stories: {user_stories}")
            for task in user_stories.get('tasks', []):
                task_description = task.get('description', 'No description provided')
                code_snippet = task.get('code_snippet', 'function_to_test(1)')
                unit_tests = generate_unit_tests(task_description, code_snippet)
                if unit_tests:
                    send_to_next_queue(unit_tests, UNIT_TEST_QUEUE)

        channel.basic_consume(queue=APPROVAL_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the approval queue")
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
