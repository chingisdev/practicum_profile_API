import logging

from kafka.admin import KafkaAdminClient, NewTopic  # type: ignore


def ensure_topic_exists(
    topic_name: str,
    num_partitions: int = 1,
    replication_factor: int = 1,
    bootstrap_servers: str = 'localhost:9092',
) -> None:
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    existing_topics = admin_client.list_topics()

    if topic_name not in existing_topics:
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        admin_client.create_topics([topic])
        logging.info('Topic {name} created!'.format(name=topic_name))
    else:
        logging.info('Topic {name} already exists!'.format(name=topic_name))
