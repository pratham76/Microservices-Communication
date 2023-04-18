FROM python:3.9

WORKDIR /app

COPY consumer_four.py .
RUN pip install pymongo

RUN pip install pika psycopg2

CMD [ "python", "./consumer_four.py" ]

