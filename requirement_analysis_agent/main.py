from dotenv import load_dotenv
import os
import pika
import json
import spacy

load_dotenv()

nlp = spacy.load("en_core_web_sm")

def analyze_requirements(requirements):
    doc = nlp(requirements["text"])
    valid = True  # Add more validation logic here
    if valid:
        return {"status": "valid", "analysis": [(ent.text, ent.label_) for ent in doc.ents]}
    else:
        return {"status": "invalid", "message": "Please provide more details"}

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='requirements_queue')

    def callback(ch, method, properties, body):
        requirements = json.loads(body)
        analysis = analyze_requirements(requirements)
        if analysis["status"] == "valid":
            send_to_next_queue(analysis, 'analysis_queue')
        else:
            send_to_next_queue(analysis, 'requirements_queue')

    channel.basic_consume(queue='requirements_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def send_to_next_queue(message, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

if __name__ == "__main__":
    receive_from_queue()
