from confluent_kafka import Producer

from resistant_kafka.producer_schemas import ProducerConfig, DataSend


class ProducerInitializer:
    def __init__(
            self,
            config: ProducerConfig,
    ):
        self._producer_name = config.producer_name
        self._producer = Producer(self._set_producer_config(config=config))

    @staticmethod
    def _set_producer_config(config: ProducerConfig) -> dict:
        producer_config = {
            'bootstrap.servers': config.bootstrap_servers,
        }
        if config.secured:
            producer_config['oauth_cb'] = config.oauth_cb
            producer_config['security.protocol'] = config.security_protocol
            producer_config['sasl.mechanisms'] = config.sasl_mechanisms

        return producer_config

    @staticmethod
    def _delivery_report(error_message, message):
        if error_message is not None:
            print("Delivery failed for User record {}: {}".format(message.key(), error_message))
            return
        print(
            "User record {} successfully produced to {} [{}] at offset {}".format(
                message.key(),
                message.topic(),
                message.partition(),
                message.offset()
            )
        )

    def send_message(
            self,
            data_to_send: DataSend,
    ):
        self._producer.produce(
            topic=self._producer_name,
            key=data_to_send.key,
            value=data_to_send.value,
            on_delivery=self._delivery_report,
            headers=data_to_send.headers
        )
        self._producer.flush()
