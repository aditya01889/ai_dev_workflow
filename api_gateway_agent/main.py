from dotenv import load_dotenv
import os
import pika
import json
import openai
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# RabbitMQ connection parameters
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
APPROVAL_QUEUE = os.getenv('APPROVAL_QUEUE', 'approval_queue')
API_GATEWAY_QUEUE = os.getenv('API_GATEWAY_QUEUE', 'api_gateway_queue')

def generate_api_gateway(task_description):
    """Generate API gateway code using OpenAI gpt-4o based on task description."""
    try:
        prompt = f"Generate an API gateway in Node.js to handle the following task: {task_description}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-05-13",  # Use the gpt-4o model
            messages=[
                {"role": "system", "content": "You are an assistant that generates API gateway code."},
                {"role": "user", "content": prompt}
            ]
        )
        gateway_code = response['choices'][0]['message']['content'].strip()
        logger.info(f"Generated API gateway code for task '{task_description}': {gateway_code}")
        return gateway_code
    except Exception as e:
        logger.error(f"Failed to generate API gateway code for task '{task_description}': {e}")
        return ""

def receive_from_queue():
    """Receive messages from the approval queue and generate API gateways."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=APPROVAL_QUEUE)

        def callback(ch, method, properties, body):
            user_stories = json.loads(body)
            logger.info(f"Received user stories: {user_stories}")
            for task in user_stories.get('tasks', []):
                task_description = task.get('description', 'No description provided')
                gateway_code = generate_api_gateway(task_description)
                if gateway_code:
                    send_to_next_queue(gateway_code, API_GATEWAY_QUEUE)

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
