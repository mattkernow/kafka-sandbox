docker-compose up -d

docker-compose scale kafka=3

List topics:
./opt/kafka_2.12-2.3.0/bin/kafka-topics.sh --zookeeper zookeeper:2181 --list

Create topic:
./opt/kafka_2.12-2.3.0/bin/kafka-topics.sh --zookeeper zookeeper:2181 --topic first_topic --create --partitions 3 --replication-fa
ctor 2

Delete topic:
./opt/kafka_2.12-2.3.0/bin/kafka-topics.sh --zookeeper zookeeper:2181 --topic first_topic --delete

Produce test message
./opt/kafka_2.12-2.3.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic first_topic
>hello

Read the test message:
./opt/kafka_2.12-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic first_topic --from-beginning
hello

Config file locations:
server config: /opt/kafka_2.12-2.3.0/config/server.properties