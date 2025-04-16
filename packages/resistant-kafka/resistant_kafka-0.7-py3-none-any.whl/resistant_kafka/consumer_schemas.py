from typing import Union, Callable

from pydantic import BaseModel, root_validator


class ConsumerConfig(BaseModel):
    """
        Configuration settings for a Kafka consumer.

        topic_to_subscribe: str -- Kafka topic, that specific processor will process
        processor_name: str -- This name can be random, just for logging
        bootstrap_servers: str -- This attribute uses for connection to Kafka server, where user try to connect
        group_id: str -- Consumer name, which would be shown as subscribed to specific topic
        auto_offset_reset: Literal ['latest', 'earliest'] -- When the group is first created, before any
                                                            messages have been consumed, the position is set a
                                                            ccording to a configurable offset reset policy
        enable_auto_commit: bool -- If True: Kafka Consumer automatically commits message offsets
                                        at a specified time interval (every 5 seconds).
                                    If False: Ensure that offset is only saved after the message
                                        has been successfully processed.
        secured: bool -- Uses to determine if it required to get JWT token for security
        oauth_cb: Callable | None -- A function that returns a token for authentication.
                                    Required only if `secured` is True.
        security_protocol: str -- The protocol used to communicate with Kafka brokers
                                  (e.g., 'SASL_PLAINTEXT', 'SASL_SSL').
        sasl_mechanisms: str -- The SASL mechanism used for authentication (e.g., 'PLAIN', 'SCRAM-SHA-256').
    """
    topic_to_subscribe: str
    processor_name: str
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = 'latest'
    enable_auto_commit: bool = True
    secured: bool = False
    oauth_cb: Union[Callable, None] = None
    security_protocol: Union[str, None] = None
    sasl_mechanisms: Union[str, None] = None

    @classmethod
    @root_validator
    def check_secured_config(cls, values):
        if values.get('secured'):
            missing_fields = []
            if values.get('oauth_cb') is None:
                missing_fields.append("oauth_cb")
            if values.get('security_protocol') is None:
                missing_fields.append("security_protocol")
            if values.get('sasl_mechanisms') is None:
                missing_fields.append("sasl_mechanisms")

            if missing_fields:
                raise ValueError(
                    f"If 'secured' is True, the following fields must be set: {', '.join(missing_fields)}"
                )
        return values
