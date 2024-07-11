from dotenv import load_dotenv
import os
import pika
import json
import subprocess
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
FRONTEND_COMPONENT_QUEUE = os.getenv('FRONTEND_COMPONENT_QUEUE', 'frontend_component_queue')
BACKEND_MICROSERVICE_QUEUE = os.getenv('BACKEND_MICROSERVICE_QUEUE', 'backend_microservice_queue')
DATABASE_SCHEMA_QUEUE = os.getenv('DATABASE_SCHEMA_QUEUE', 'database_schema_queue')
API_GATEWAY_QUEUE = os.getenv('API_GATEWAY_QUEUE', 'api_gateway_queue')
DEPLOYMENT_QUEUE = os.getenv('DEPLOYMENT_QUEUE', 'deployment_queue')

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

def execute_unit_tests(tests):
    """Execute the generated unit tests and return the results."""
    test_file = 'test_file.py'
    with open(test_file, 'w') as f:
        f.write(tests)
    
    try:
        result = subprocess.run(['pytest', test_file], capture_output=True, text=True)
        logger.info(f"Executed unit tests with result: {result.stdout}")
        return result.stdout
    except Exception as e:
        logger.error(f"Failed to execute unit tests: {e}")
        return str(e)

def receive_from_queue():
    """Receive messages from the unit test queue and generate unit tests."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=UNIT_TEST_QUEUE)

        def callback(ch, method, properties, body):
            task = json.loads(body)
            logger.info(f"Received task: {task}")

            if task.get('approved', False):
                task_description = task.get('description', 'No description provided')
                code_snippet = task.get('code_snippet', 'function_to_test(1)')
                unit_tests = generate_unit_tests(task_description, code_snippet)
                if unit_tests:
                    test_results = execute_unit_tests(unit_tests)
                    task['unit_test_results'] = test_results
                    queue_name = determine_queue(task_description)
                    if queue_name:
                        send_to_next_queue(task, queue_name)
                    else:
                        logger.error(f"Could not determine the next queue for task: {task_description}")
            else:
                logger.info("Task not approved, skipping.")

        channel.basic_consume(queue=UNIT_TEST_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the unit test queue")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Failed to receive from queue: {e}")
        raise

def determine_queue(task_description):
    """Determine the next queue based on the task type."""
    if "frontend" in task_description.lower():
        return FRONTEND_COMPONENT_QUEUE
    elif "backend" in task_description.lower():
        return BACKEND_MICROSERVICE_QUEUE
    elif "database" in task_description.lower():
        return DATABASE_SCHEMA_QUEUE
    elif "api gateway" in task_description.lower():
        return API_GATEWAY_QUEUE
    return None

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
