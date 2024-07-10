from dotenv import load_dotenv
import os
import pika
import json
import random

load_dotenv()

def estimate_effort(task):
    return random.randint(1, 10)

def create_user_stories(analysis):
    tasks = ["Build frontend", "Create backend API", "Design database schema"]
    task_estimates = {task: estimate_effort(task) for task in tasks}
    return task_estimates

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='analysis_queue')

    def callback(ch, method, properties, body):
        analysis = json.loads(body)
        user_stories = create_user_stories(analysis)
        send_to_next_queue(user_stories, 'approval_queue')

    channel.basic_consume(queue='analysis_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def send_to_next_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

if __name__ == "__main__":
    receive_from_queue()
