from typing import Union

from pydantic import BaseModel

from resistant_kafka.common_schemas import KafkaSecurityConfig


class ConsumerConfig(BaseModel):
    """
        Configuration settings for a Kafka consumer.

        :param: topic_to_subscribe: str -- Kafka topic, that specific processor will process
        :param: processor_name: str -- This name can be random, just for logging
        :param: bootstrap_servers: str -- This attribute uses for connection to Kafka server, where user try to connect
        :param:  group_id: str -- Consumer name, which would be shown as subscribed to specific topic
        :param: auto_offset_reset: Literal ['latest', 'earliest'] -- When the group is first created, before any
                                                            messages have been consumed, the position is set according
                                                            to a configurable offset reset policy
        :param: enable_auto_commit: bool -- If True: Kafka Consumer automatically commits message offsets
                                        at a specified time interval (every 5 seconds).
                                    If False: Ensure that offset is only saved after the message
                                        has been successfully processed.
    """
    topic_to_subscribe: str
    processor_name: str
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = 'latest'
    enable_auto_commit: bool = True
    security_config: Union[KafkaSecurityConfig, None] = False
