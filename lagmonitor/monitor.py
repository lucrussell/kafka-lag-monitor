import statsd
from pykafka import KafkaClient


class Monitor:

    def __init__(self, config=None):
        self.brokers = config['monitor']['brokers']
        self.consumer_groups = config['monitor']['consumer_groups']
        self.statsd_client = statsd.StatsClient(config['monitor']['statsd']['host'],
                                                config['monitor']['statsd']['port'],
                                                config['monitor']['statsd']['prefix'])

    def report(self):
        kafka_client = KafkaClient(hosts=','.join(self.brokers))
        for topic_name, value in self.consumer_groups.items():
            group_name = value['group_name']
            topic = kafka_client.topics[topic_name.encode('utf-8')]
            lag_report = self.get_lag(topic, group_name.encode('utf-8'))

            # Check the lag for all partitions, for every specified topic
            # The resulting statsd metric will look something like this: 'group_id_1.topic1.0.offset'
            for partition, offset_lag in lag_report.items():
                group_topic_partition_offset = '{0}.{1}.{2}.{3}'.format(group_name, topic_name, partition, 'offset')
                group_topic_partition_lag = '{0}.{1}.{2}.{3}'.format(group_name, topic_name, partition, 'lag')

                print("Setting: {0} to {1}".format(group_topic_partition_offset, offset_lag[0]))
                self.statsd_client.gauge(group_topic_partition_offset, offset_lag[0])
                lag = offset_lag[0] - offset_lag[1]
                print("Setting: {0} to {1}".format(group_topic_partition_lag, lag))
                self.statsd_client.gauge(group_topic_partition_lag, lag)

    def get_lag(self, topic, consumer_group):
        latest_offsets = topic.latest_available_offsets()
        consumer = topic.get_simple_consumer(consumer_group=consumer_group, auto_start=False)
        current_offsets = consumer.fetch_offsets()
        consumer.stop()
        return {p_id: (latest_offsets[p_id].offset[0], res.offset)
                for p_id, res in current_offsets}
