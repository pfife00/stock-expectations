
<h2>Setting up kafka</h2>
kakfa was setup using pegasus

<h3>Testing out topics locally (on kafka node)</h3>

<h4>First create the topics</h4>
The code below will create a test topic<br>

<code>/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 3 --topic test_topic</code><br>

where:<br>
<ul>
    <li>replication-factor sets how many times a topic is replicated in kafka for fault tolerance</li>
    <li>partitions sets the number of kafka partitions</li>
    <li>topic creates the kafka topic</li>
    </ul>
    
<h4>View a topic</h4>
An existing topic can be viewed by running the code below:<br>
<code>/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181</code>

<h4>Write messages from the console</h4>
First run the code below create producer<br>
<code>/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test</code><br>

Then run the below code:<br>
<code>echo "my test message" | /usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic price</code>

<h4>Read from the console</h4>
Run the command below to read from console<br>
<code>/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning</code>

<h4>Run Producer</h4>
Use the below code to run the producer<br>
<code>/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic price --from-beginning</code>


```python

```
