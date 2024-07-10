from dotenv import load_dotenv
import os
import pika
import json
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_frontend_component(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='approval_queue')

    def callback(ch, method, properties, body):
        user_stories = json.loads(body)
        component_code = generate_frontend_component("Generate a React component for a login form with username and password fields.")
        send_to_next_queue(component_code, 'approval_queue')

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
