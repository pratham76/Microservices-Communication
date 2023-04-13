import pika

# RabbitMQ connection parameters
hostname = 'rabbitmq'
port = 5672
virtual_host = '/'
username = 'guest'
password = 'guest'

# Establish connection with RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname, port, virtual_host, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange='student_management', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='student_management', queue='health_check', routing_key='health_check')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# Set up consumer to listen for messages on queue
channel.basic_consume(queue='health_check', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for health check messages. To exit press CTRL+C')
channel.start_consuming()
