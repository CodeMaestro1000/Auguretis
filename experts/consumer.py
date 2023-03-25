from repository import make_bigquery_request
import pika, json, redis, zlib
import logging
from core import settings
from main import client

logging.basicConfig(level=logging.INFO)


AMPQ_URL = settings.AMPQ_URL
REDIS_URL = settings.REDIS_URL
params = pika.URLParameters(AMPQ_URL)

connection = pika.BlockingConnection(params)
redis_pool = redis.ConnectionPool().from_url(REDIS_URL)
redis_connection = redis.Redis(connection_pool=redis_pool)

channel = connection.channel()

channel.queue_declare(queue='experts')

def check_for_cached(query):
    hash = zlib.adler32(query.encode('utf-8'))
    data = redis_connection.get(hash)
    if data:
        return json.loads(data)
    return None

def write_to_cache(query, result):
    hash = zlib.adler32(query.encode('utf-8'))
    redis_connection.set(hash, json.dumps(result))

def callback(channel, method, properties: pika.BasicProperties, body):
    logging.info('========= Recieved in Experts ============')
    body = json.loads(body)
    response = ''
    if properties.content_type == "get experts":
        logging.info(f"Expert request for {body}, processing...")
        cached_response = check_for_cached(body)
        if not cached_response:
            payload = make_bigquery_request(client, body)
            response = json.dumps(payload)
            write_to_cache(body, response)
        else:
            logging.info(f"Returning cached result...")
            response = cached_response

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id = properties.correlation_id),
        body=response
    )
    
    channel.basic_ack(delivery_tag=method.delivery_tag)


# channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='experts', on_message_callback=callback)

logging.info('Started Consuming')

channel.start_consuming()

channel.close()