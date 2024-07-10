from dotenv import load_dotenv
import os
import pika
import json
import subprocess
import time

load_dotenv()

def deploy_application():
    subprocess.run(["docker-compose", "up", "-d"])

def check_service(service_name):
    status = subprocess.run(["systemctl", "is-active", "--quiet", service_name])
    return status.returncode == 0

def restart_service(service_name):
    subprocess.run(["systemctl", "restart", service_name])

def self_heal():
    services = ["docker", "jenkins"]
    while True:
        for service in services:
            if not check_service(service):
                print(f"{service} is down. Restarting...")
                restart_service(service)
        time.sleep(60)

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='approval_queue')

    def callback(ch, method, properties, body):
        user_stories = json.loads(body)
        deploy_application()
        send_to_next_queue({"status": "Deployed"}, 'approval_queue')

    channel.basic_consume(queue='approval_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def send_to_next_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

if __name__ == "__main__":
    self_heal()
    receive_from_queue()
