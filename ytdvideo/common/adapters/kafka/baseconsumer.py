import json
import logging
from typing import Dict

from confluent_kafka.cimpl import Consumer

from common.adapters.kafka.types import TPayload, TMessage


logger = logging.getLogger("vikas.event.kafka.log")


class BaseConsumer:
    config = None
    topics: list = []
    payload_class = None
    message_class = None

    def __init__(self):
        self.consumer = Consumer(self.config)
        self.consumer.subscribe(self.topics)

    def get_payload_class(self, *args, **kwargs):
        assert hasattr(self, "payload_class"), (
            f"Please specify the `payload_class` in {self.__class__.__name__}."
        )
        return getattr(self, "payload_class")

    def get_message_class(self, *args, **kwargs):
        assert hasattr(self, "message_class"), (
            f"Please specify the `message_class` in {self.__class__.__name__}"
        )
        return getattr(self, "message_class")

    def get_payload(self, payload_cls: TPayload, message_dict: Dict):
        return payload_cls.to_instance(**message_dict)

    def get_message(self, message_cls: TMessage, message_dict: Dict):
        return message_cls.to_instance(**message_dict)

    def process_message(self, msg):
        message_dict = json.loads(msg.value())

        # get payload and convert it into subtype of Payload class
        payload = message_dict["payload"]
        payload = self.get_payload(self.get_payload_class(), payload)
        message_dict["payload"] = payload

        message = self.get_message(self.get_message_class(), message_dict)
        return message

    def handle_message(self, message: TMessage):
        raise NotImplementedError("Please Implement `handle_message` method.")

    # todo: Error Handling
    def consume(self):
        while True:
            try:
                msg = self.consumer.poll(1.0)
                if msg:
                    message = self.process_message(msg)
                    self.handle_message(message=message)
            except Exception:
                logger.error(f"Error in Consume of"
                             f" {self.__class__.__name__}.", exc_info=True)

