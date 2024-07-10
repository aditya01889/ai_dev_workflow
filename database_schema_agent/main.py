from dotenv import load_dotenv
import os
import pika
import json

load_dotenv()

def generate_database_schema():
    schema = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );

    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        stock INT NOT NULL
    );
    """
    return schema

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='approval_queue')

    def callback(ch, method, properties, body):
        user_stories = json.loads(body)
        schema_code = generate_database_schema()
        send_to_next_queue(schema_code, 'approval_queue')

    channel.basic_consume(queue='approval_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def send_to_next_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

if __name__ == "__main__":
    receive_from_queue()
