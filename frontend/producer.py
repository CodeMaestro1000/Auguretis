import pika, json, uuid
from config.settings import AMPQ_URL


class CreateRpcClient:

    def __init__(self, url=AMPQ_URL):
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        """Where the returned response is tored in response"""
        if self.corr_id == props.correlation_id:
            self.response = body

    async def pubilsh(self, data, content_type, routing_key='main'): # to await in route
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id, content_type=content_type), 
            body=json.dumps(data)
        )
        self.connection.process_data_events(time_limit=None)
        return self.response
