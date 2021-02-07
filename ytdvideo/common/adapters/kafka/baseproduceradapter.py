import logging
from datetime import datetime
from typing import Type, cast, Union, Any, Optional

from common.adapters.kafka.types import TPayload, Payload, TMessage

logger = logging.getLogger("vikas.event.kafka.log")


class BaseProducerAdapter:
    kafka_producer_class = None
    topics = []
    payload_class = None
    message_class = None

    def get_kafka_producer(self):
        """Override this method to get the kafka_producer."""
        return self.kafka_producer_class()

    def get_topics(self):
        """You can override this method to set which topic to write"""
        return self.topics

    def get_partition(self, topic) -> Optional[int]:
        """You can override this method to set which partition to write based on the topic"""
        return None

    def get_payload_class(self) -> Type[TPayload]:
        """You can override this method to set custom logic for fetching payload_class"""
        assert self.payload_class is not None, (
            "Please provide a `payload_class` or override the `get_payload_class()` method"
        )
        return self.payload_class

    def get_payload(self, payload_cls: Type[TPayload],
                    data: Union[Payload, Any]) -> TPayload:
        """You can override this method to set custom logic to get the payload.
        If you send the paylod object as data then it'll return the same object

        If you send anything other than an object of type/subtype payload, then you need to implement
        `to_instance()` for that type/sub-type.
        """
        if isinstance(data, Payload):
            return cast(TPayload, data)

        payload = payload_cls
        assert getattr(payload, "to_instance", None), (
            f"Please make sure class: {payload.__class__.__name__} implements"
            f"`to_instance()` method"
        )
        return payload.to_instance(**data)

    def get_message_class(self) -> Type[TMessage]:
        """Overide this method to set custom logic for retrieving the message class"""
        assert self.message_class is not None, (
            "Please provide a `message_class` or override the `get_message_class` method"
        )
        return self.message_class

    def get_message(
            self,
            message_cls: Type[TMessage],
            payload: TPayload,
            message_type: str = "",
            timestamp: datetime = None
    ) -> TMessage:
        """Overide this method to change the way in which the message is created.

        Args:
            message_cls: subclass of `Message`. Should have a `to_instance()` method
            payload: sublass of `Payload`
            message_type: type of the Message [Defaults to the kafka_producer_class name]
            timestamp: the timestamp of the message
        Returns:
            An instance of message_cls

        """

        assert isinstance(payload, Payload), (
            f"payload has to be a subclass to class: Payload"
        )
        assert getattr(message_cls, "to_instance", None), (
            f"Please make sure class: {message_cls.__class__.__name__} implements"
            f"`to_instance()` method class method"
        )
        return message_cls(
            payload=payload,
            message_type=message_type or self.kafka_producer_class.__name__,
            timestamp=timestamp
        )

    def sync_produce(
            self,
            kafka_producer,
            topic: str,
            message: TMessage,
            partition: Optional[int] = None
    ):

        if partition:
            kafka_producer.sync_produce_to_partition(
                topic=topic,
                message=message,
                partition=partition
            )
        else:
            kafka_producer.sync_produce(
                topic=topic,
                message=message
            )

    def async_produce(
            self,
            kafka_producer,
            topic: str,
            message: TMessage,
            partition: Optional[int] = None):

        if partition:
            kafka_producer.produce_to_partition(
                topic=topic,
                message=message,
                partition=partition
            )
        else:
            kafka_producer.produce(
                topic=topic,
                message=message
            )

    def produce(
            self,
            payload: Union[TPayload, Any],
            message_type: str = "",
            timestamp: datetime = None,
            sync: bool = False
    ):
        topics = self.get_topics()
        payload = self.get_payload(self.get_payload_class(), payload)
        message = self.get_message(
            message_cls=self.get_message_class(),
            payload=payload,
            message_type=message_type,
            timestamp=timestamp
        )
        kafka_producer = self.get_kafka_producer()

        for topic in topics:
            partition = self.get_partition(topic)
            if sync:
                self.sync_produce(kafka_producer, topic, message, partition)
            else:
                self.async_produce(kafka_producer, topic, message, partition)
