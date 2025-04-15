import asyncio
import functools
import logging
from abc import abstractmethod
from typing import Any

from confluent_kafka import Consumer

from resistant_kafka.common_exceptions import KafkaMessageError
from resistant_kafka.consumer_schemas import ConsumerConfig

logging.basicConfig(level=logging.INFO)


class ConsumerInitializer:
    def __init__(
            self,
            config: ConsumerConfig
    ):
        self._consumer = Consumer(
            self._set_consumer_config(config=config)
        )
        self._consumer.subscribe(
            topics=[config.topic_to_subscribe],
            on_assign=self._connection_flag_method
        )
        self._config = config

    @staticmethod
    def _set_consumer_config(config: ConsumerConfig) -> dict:
        consumer_config = {
            'bootstrap.servers': config.bootstrap_servers,
            'group.id': config.group_id,
            'auto.offset.reset': config.auto_offset_reset,
            'enable.auto.commit': config.enable_auto_commit
        }
        if config.secured:
            consumer_config['oauth_cb'] = config.oauth_cb
            consumer_config['security.protocol'] = config.security_protocol
            consumer_config['sasl.mechanisms'] = config.sasl_mechanisms

        return consumer_config

    def _connection_flag_method(self, *args):
        logging.info(f"{self._config.processor_name} successful subscribed "
                     f"to the topic {self._config.topic_to_subscribe}\n")

    @staticmethod
    def message_is_empty(message: Any, consumer: Consumer):
        if message is None:
            consumer.commit(asynchronous=True)
            return True

        if getattr(message, "key", None) is None:
            consumer.commit(asynchronous=True)
            return True

        if message.key() is None:
            consumer.commit(asynchronous=True)
            return True

        return False

    @staticmethod
    async def get_message(consumer):
        loop = asyncio.get_running_loop()
        poll = functools.partial(consumer.poll, 1.0)
        return await loop.run_in_executor(executor=None, func=poll)

    @abstractmethod
    async def process(self):
        pass


def kafka_processor(raise_error=False):
    def handle_kafka_errors(func):
        async def wrapper(self, *args, **kwargs):
            while True:
                try:
                    await func(self, *args, **kwargs)
                except Exception as e:
                    if raise_error:
                        raise KafkaMessageError(str(e))

                    print(f"Kafka processing error: {e}")

                finally:
                    self._consumer.commit(asynchronous=True)

        return wrapper

    return handle_kafka_errors


async def process_kafka_connection(tasks: list[ConsumerInitializer]):
    while True:
        await asyncio.gather(*[task.process() for task in tasks])


def init_kafka_connection(tasks: list[ConsumerInitializer]):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(process_kafka_connection(tasks=tasks))

    loop.run_forever()
