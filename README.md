# Kafka Lag Monitor

An application to periodically query Kafka lag metrics and send to statsd.

## Set Up
To build and run:

```
$ docker-compose up -d
```

This assumes entries for Kafka and Zookeeper in /etc/hosts, i.e.:

```
127.0.0.1 kafka
127.0.0.1 zookeeper
```

## Viewing Lag Graphs with Grafana 
The Grafana image bundled in the Compose file is documented [here](https://github.com/samuelebistoletti/docker-statsd-influxdb-grafana).

1. Set up the Grafana datasource using the instructions provided at the link above.
2. Send some example messages to the test topic, e.g. with `kafkacat`: `echo "foo" | kafkacat -b kafka:9092 -t topic1`. Here is a [quick reference](http://lucrussell.com/kafkacat-quick-reference/) for kafkacat.
3. After doing so, you should be able to set up a dashboard like the one shown below.
4. The metric to select from will be in the format `lagmonitor.<group_name>.<topic_name>.<partition_id>.lag`, for example `lagmonitor.group_id_1.topic1.0.lag`.

![Grafana Example](grafana_example.png) 