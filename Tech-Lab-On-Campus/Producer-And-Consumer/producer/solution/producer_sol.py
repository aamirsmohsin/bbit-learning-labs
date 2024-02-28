import sys
sys.path.insert(1, '/app/Producer-And-Consumer/producer')

from producer_interface import mqProducerInterface
import pika
import os

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        
        self.channel = None
        self.connection = None

        self.setupRMQConnection()

    def setupRMQConnection(self):
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)

        self.connection = connection
        self.channel = connection.channel()

        exchange = self.channel.exchange_declare(exchange=self.exchange_name)

    def publishOrder(self, message: str):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body="Message",
        )

        print("order published")

        self.channel.close()
        self.connection.close()