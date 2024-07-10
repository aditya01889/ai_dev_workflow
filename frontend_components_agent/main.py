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
FRONTEND_COMPONENT_QUEUE = os.getenv('FRONTEND_COMPONENT_QUEUE', 'frontend_component_queue')

def generate_frontend_component(task_description):
    """Generate frontend component code using OpenAI gpt-4o."""
    try:
        prompt = f"Generate a React component for the following task: {task_description}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-05-13",  # Use the gpt-4o model
            messages=[
                {"role": "system", "content": "You are an assistant that generates code."},
                {"role": "user", "content": prompt}
            ]
        )
        component_code = response['choices'][0]['message']['content'].strip()
        logger.info(f"Generated component code for task '{task_description}': {component_code}")
        return component_code
    except Exception as e:
        logger.error(f"Failed to generate component code for task '{task_description}': {e}")
        return ""

def receive_from_queue():
    """Receive messages from the approval queue and generate frontend components."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=APPROVAL_QUEUE)

        def callback(ch, method, properties, body):
            user_stories = json.loads(body)
            logger.info(f"Received user stories: {user_stories}")
            for task in user_stories.get('tasks', []):
                task_description = task.get('description', 'No description provided')
                component_code = generate_frontend_component(task_description)
                if component_code:
                    send_to_next_queue(component_code, FRONTEND_COMPONENT_QUEUE)

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
