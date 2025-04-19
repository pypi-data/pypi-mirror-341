from dataclasses import dataclass
from typing import Any, Union

from pydantic import BaseModel

from resistant_kafka_avataa.common_schemas import KafkaSecurityConfig


class ProducerConfig(BaseModel):
    """
        Configuration settings for a Kafka producer.

        :param bootstrap_servers: str -- Kafka server address to connect the producer.
        :param producer_name: str -- Name for identifying the producer (used mainly for logging/debugging).
    """
    bootstrap_servers: str
    producer_name: str
    security_config: Union[KafkaSecurityConfig, None] = None


@dataclass
class DataSend:
    key: str
    value: Any
    headers: list[tuple] | None = None
