import pika
import json
import time
import pymongo
import json

# Set up MongoDB client
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["studentdatabase"]
collection = db["students"]
time.sleep(9)
# Set up RabbitMQ connection
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

# Declare queue and callback function
channel.queue_declare(queue='insert_record')

def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(data)
    name = data['name']
    srn = data['srn']
    section = data['section']

    # Insert data into MongoDB
    student_data = {"name": name, "srn": srn, "section": section}
    collection.insert_one(student_data)

    print("Data inserted into MongoDB:", student_data)

channel.basic_consume(queue='insert_record', on_message_callback=callback)

print('Waiting for insert record messages...')
channel.start_consuming()

