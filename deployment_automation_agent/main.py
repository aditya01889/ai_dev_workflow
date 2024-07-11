from dotenv import load_dotenv
import os
import pika
import json
import subprocess
import time
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
UNIT_TEST_QUEUE = os.getenv('UNIT_TEST_QUEUE', 'unit_test_queue')
DEPLOYMENT_QUEUE = os.getenv('DEPLOYMENT_QUEUE', 'deployment_queue')

def deploy_application():
    """Deploy the application using Docker Compose."""
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        logger.info("Application deployed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to deploy application: {e}")

def check_service(service_name):
    """Check if a service is active."""
    status = subprocess.run(["systemctl", "is-active", "--quiet", service_name])
    return status.returncode == 0

def restart_service(service_name):
    """Restart a service."""
    try:
        subprocess.run(["systemctl", "restart", service_name], check=True)
        logger.info(f"{service_name} restarted successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart {service_name}: {e}")

def self_heal():
    """Continuously monitor and restart services if they go down."""
    services = ["docker", "jenkins"]
    while True:
        for service in services:
            if not check_service(service):
                logger.warning(f"{service} is down. Restarting...")
                restart_service(service)
        time.sleep(60)

def receive_from_queue():
    """Receive messages from the unit test queue and deploy the application if all defects are resolved."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=UNIT_TEST_QUEUE)

        def callback(ch, method, properties, body):
            task = json.loads(body)
            logger.info(f"Received task: {task}")

            if task.get('unit_test_results') and "All tests passed" in task['unit_test_results']:
                deploy_application()
                send_to_next_queue({"status": "Deployed"}, DEPLOYMENT_QUEUE)
            else:
                logger.info("Defects found or tests not passed. Deployment skipped.")

        channel.basic_consume(queue=UNIT_TEST_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info("Started consuming from the unit test queue")
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
    # Start self-healing in a separate thread
    import threading
    threading.Thread(target=self_heal, daemon=True).start()

    # Start consuming messages from the queue
    receive_from_queue()
