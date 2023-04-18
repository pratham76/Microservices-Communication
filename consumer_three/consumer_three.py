import pymongo
import time
import pika
import json

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["studentdatabase"]
collection = db["students"]

def delete_student(srn):
    query = {"srn": srn}
    result = collection.delete_one(query)
    return result.deleted_count > 0

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
channel.queue_declare(queue='delete_record')

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received delete record message: {data}")
    
    srn = data['srn']
    if delete_student(srn):
        print(f"Deleted record with SRN: {srn}")
    else:
        print(f"Record with SRN {srn} not found")

channel.basic_consume(queue='delete_record', on_message_callback=callback)
print('Waiting for delete record messages...')
channel.start_consuming()
