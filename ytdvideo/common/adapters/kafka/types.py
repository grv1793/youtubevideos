from datetime import datetime, timezone
from typing import Dict, TypeVar, Type, Union, Optional

TMessage = TypeVar("TMessage", bound="Message")
TPayload = TypeVar("TPayload", bound="Payload")


class Payload:

    @classmethod
    def to_instance(cls: Type[TPayload], *args, **kwargs) -> TPayload:
        raise NotImplementedError(
            f"Not Implemented `to_instance` method for class: "
            f"{cls.__name__}"
        )

    def to_dict(self):
        raise NotImplementedError(
            f"Not Implemented to_dict() method for class: "
            f"{self.__class__.__name__}")


class Message:
    datetime_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self,
                 payload: TPayload,
                 message_type: str,
                 timestamp: Optional[datetime] = None
    ) -> None:
        self.payload = payload
        self.message_type = message_type
        if timestamp:
            assert isinstance(timestamp, datetime) is True
            self._timestamp = timestamp.replace(tzinfo=timezone.utc).strftime(self.datetime_format)

    @property
    def timestamp(self) -> str:
        if not getattr(self, "_timestamp", None):
            self._timestamp = datetime.now().replace(tzinfo=timezone.utc).strftime(self.datetime_format)
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: Optional[datetime] = None) -> None:
        if isinstance(timestamp, datetime):
            # this will be called when timestamp is set outside of constructor and when timestamp is valid
            self._timestamp = timestamp.replace(tzinfo=timezone.utc).strftime(self.datetime_format)
        raise ValueError(f"Expected Type: datetime.datetime. Received Type: {type(self.timestamp)}")

    def to_dict(self) -> Dict[str, Union[Dict, str]]:
        return {
            'payload': self.payload.to_dict(),
            'message_type': self.message_type,
            'timestamp': self.timestamp
        }

    @classmethod
    def to_instance(
            cls: Type[TMessage],
            payload: TPayload,
            message_type: str,
            timestamp: Union[str, datetime] = None
    ) -> TMessage:
        """Converts the given data into an instance of type/subtype `Message`
        Args:
            `payload`: This should be of type `Payload` or a subclass of `Payload`
            `message_type`: A string which specifies the type of message or it can specify anything that you.
                Can be used on the consumer to differentiate messages.
            `timestamp`: datetime object
        Returns:
            An instance of the type/subtype Message.

        """
        assert isinstance(payload, Payload) is True, (
            f"The `payload` sent to {cls.__name__} method does not seem to a subclass of `Payload`."
            f"Please overide the existing implementation of `to_instance()` to support your type."
        )
        assert isinstance(message_type, str) is True, (
            f"Please make sure that `action` message_type is a string. "
            f"You can change the message_type by overriding the `to_instance()` of {cls.__name__}"
        )

        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.strptime(timestamp, cls.datetime_format)

        return cls(payload, message_type, timestamp)