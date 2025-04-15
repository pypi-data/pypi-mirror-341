from dataclasses import dataclass
from typing import Callable, Any, Union

from pydantic import BaseModel, root_validator


class ProducerConfig(BaseModel):
    """
        bootstrap_servers: str -- This attribute uses for connection to Kafka server, where user try to connect
        producer_name: str -- This attribute uses for connection to Kafka server, where user try to connect

    """
    bootstrap_servers: str
    producer_name: str
    secured: bool
    oauth_cb: Union[Callable, None] = None
    security_protocol: Union[str, None] = None
    sasl_mechanisms: Union[str, None] = None

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
