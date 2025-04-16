from dataclasses import dataclass
from typing import Callable, Any, Union

from pydantic import BaseModel, root_validator


class ProducerConfig(BaseModel):
    """
        Configuration settings for a Kafka producer.

        bootstrap_servers: str -- Kafka server address to connect the producer.
        producer_name: str -- Name for identifying the producer (used mainly for logging/debugging).
        secured: bool -- Indicates whether secure authentication (e.g., OAuth) is required.
        oauth_cb: Callable | None -- A function used to retrieve an authentication token.
                                     Required if `secured` is True.
        security_protocol: str | None -- Protocol used to communicate with Kafka (e.g., 'SASL_PLAINTEXT', 'SASL_SSL').
        sasl_mechanisms: str | None -- SASL mechanism for authentication (e.g., 'PLAIN', 'SCRAM-SHA-256').
    """

    bootstrap_servers: str
    producer_name: str
    secured: bool
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


@dataclass
class DataSend:
    key: str
    value: Any
    headers: list[tuple] | None = None
