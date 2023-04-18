import pymongo
import time
import pika
import json
import logging
logging.basicConfig(level=logging.INFO)
mongo_client = pymongo.MongoClient("mongodb://database")
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
    logging.info("Received delete record message: %s",data)
    srn = data['srn']
    if delete_student(srn):
        logging.info(f"Deleted record with SRN: %s",data)
    else:
        logging.info(f"Record with SRN %S not found",data)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(queue='delete_record', on_message_callback=callback)
print('Waiting for delete record messages...')
channel.start_consuming()
