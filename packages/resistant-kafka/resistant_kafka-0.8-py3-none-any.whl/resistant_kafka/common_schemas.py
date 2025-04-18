from typing import Callable

from pydantic import BaseModel


class KafkaSecurityConfig(BaseModel):
    """
        Security configuration settings for a Kafka consumer. Uses as part for main config classes.

        :param Callable oauth_cb:  -- A function that returns a token for authentication.
                                Required only if `secured` is True.
        :param str security_protocol: -- The protocol used to communicate with Kafka brokers
                                  (e.g., 'SASL_PLAINTEXT', 'SASL_SSL').
        :param str sasl_mechanisms:  -- The SASL mechanism used for authentication (e.g., 'PLAIN', 'SCRAM-SHA-256').
    """
    oauth_cb: Callable
    security_protocol: str
    sasl_mechanisms: str
