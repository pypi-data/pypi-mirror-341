import json
import logging

import sentry_sdk
from time import perf_counter as time_now
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import Error as DbError
from kafka import KafkaConsumer

from promy.station.registry import station_registry
from promy.utils.monitoring import KAFKA_CONSUME_DURATION

logger = logging.getLogger("Consumer")


class Command(BaseCommand):
    def handle(self, *args, **options):
        handlers = station_registry.kafka_updater_handlers

        kafka = settings.ENV.kafka

        while True:
            consumer = KafkaConsumer(
                *handlers.keys(),
                bootstrap_servers=kafka.bootstrap_servers,
                security_protocol=kafka.security_protocol,
                sasl_mechanism=kafka.sasl_mechanism,
                sasl_plain_username=kafka.username,
                sasl_plain_password=kafka.password,
                group_id=kafka.group_id,
                enable_auto_commit=False,
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x),
                key_deserializer=lambda x: x.decode(),
            )

            for message in consumer:
                sentry_sdk.set_context(
                    "message",
                    {
                        "topic": message.topic,
                        "partition": message.partition,
                        "offset": message.offset,
                        "key": message.key,
                        "value": message.value,
                    },
                )

                start = time_now()
                success = "false"

                try:
                    handlers[message.topic](message.value)
                    success = "true"
                except DbError:
                    logger.exception(
                        "handler failed due to database issues, exiting",
                        extra={
                            "topic": message.topic,
                            "partition": message.partition,
                            "offset": message.offset,
                            "key": message.key,
                        },
                    )
                    exit(1)
                except Exception:
                    logger.exception(
                        "handler failed",
                        extra={
                            "topic": message.topic,
                            "partition": message.partition,
                            "offset": message.offset,
                            "key": message.key,
                        },
                    )
                else:
                    consumer.commit()
                    logger.info(
                        "consumer committed",
                        extra={
                            "topic": message.topic,
                            "partition": message.partition,
                            "offset": message.offset,
                            "key": message.key,
                        },
                    )

                KAFKA_CONSUME_DURATION.labels(message.topic, success).observe(
                    time_now() - start
                )
