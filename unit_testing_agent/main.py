from dotenv import load_dotenv
import os
import pika
import json

load_dotenv()

def generate_unit_tests(code_snippet):
    tests = f"""
    import pytest

    def test_function():
        result = {code_snippet}
        assert result == expected_output

    if __name__ == "__main__":
        pytest.main()
    """
    return tests

def receive_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='approval_queue')

    def callback(ch, method, properties, body):
        user_stories = json.loads(body)
        unit_tests = generate_unit_tests("function_to_test(1)")
        send_to_next_queue(unit_tests, 'approval_queue')

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
