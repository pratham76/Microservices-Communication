import pika
from flask import Flask, request

app = Flask(__name__)

# RabbitMQ connection parameters
hostname = 'rabbitmq'
port = 5672
virtual_host = '/'
username = 'guest'
password = 'guest'

# Establish connection with RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                       port,
                                       virtual_host,
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Create exchange and queues
channel.exchange_declare(exchange='student_management', exchange_type='direct')

# Queue for health check
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='student_management', queue='health_check', routing_key='health_check')

# Queue for insert record
channel.queue_declare(queue='insert_record')
channel.queue_bind(exchange='student_management', queue='insert_record', routing_key='insert_record')

# Queue for read database
channel.queue_declare(queue='read_database')
channel.queue_bind(exchange='student_management', queue='read_database', routing_key='read_database')

# Queue for delete record
channel.queue_declare(queue='delete_record')
channel.queue_bind(exchange='student_management', queue='delete_record', routing_key='delete_record')


@app.route('/health_check', methods=['GET'])
def health_check():
    # Send health check message to RabbitMQ
    channel.basic_publish(exchange='student_management', routing_key='health_check', body='RabbitMQ health check')
    return 'Health check message sent to RabbitMQ'


@app.route('/insert_record', methods=['POST'])
def insert_record():
    # Extract data from request
    name = request.form.get('Name')
    srn = request.form.get('SRN')
    section = request.form.get('Section')

    # Create message
    message = f'{name},{srn},{section}'

    # Send message to RabbitMQ
    channel.basic_publish(exchange='student_management', routing_key='insert_record', body=message)
    return f'Record for SRN {srn} added to RabbitMQ'


@app.route('/read_database', methods=['GET'])
def read_database():
    # Send message to RabbitMQ
    channel.basic_publish(exchange='student_management', routing_key='read_database', body='Read database')
    return 'Read database message sent to RabbitMQ'


@app.route('/delete_record', methods=['GET'])
def delete_record():
    # Extract SRN from request
    srn = request.args.get('SRN')

    # Create message
    message = f'{srn}'

    # Send message to RabbitMQ
    channel.basic_publish(exchange='student_management', routing_key='delete_record', body=message)
    return f'Record for SRN {srn} deleted from RabbitMQ'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
