import pymongo
import pika
import time
import json


time.sleep(9)
# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["studentdatabase"]
collection = db["students"]

hostname = '172.17.0.1'
port = 5672
virtual_host = '/'
username = 'guest'
password = 'guest'
print(hostname)
time.sleep(9)


# Establish connection with RabbitMQ
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                       port,
                                       virtual_host,
                                       credentials,heartbeat=1200)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# Declare queue and bind to exchange
channel.queue_declare(queue='read_database')
channel.queue_bind(queue='read_database', exchange='student_management', routing_key='read_database')

# Define callback function for reading from database
def read_database_callback(ch, method, properties, body):
    # Retrieve all documents in the collection
    documents = collection.find()
    # Print each document
     
    for document in documents:
        print(document)

# Consume messages from queue
channel.basic_consume(queue='read_database', on_message_callback=read_database_callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()

