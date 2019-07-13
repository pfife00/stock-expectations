
<h3>Install Kafka</h3>

<h4>Download and install the package</h4>
Note: replace the version with correct version<br>
<code>wget http://apache.claz.org/kafka/0.8.2.1/kafka\_2.9.1-0.8.2.1.tgz -P ~/Downloads </code><br>
<code>sudo tar zxvf ~/Downloads/kafka\_2.9.1-0.8.2.1.tgz -C /usr/local</code><br>
<code>$ sudo mv /usr/local/kafka_2.9.1-0.8.2.1 /usr/local/kafka</code><br>

<h3> Configure the server</h3>
On each node configure server.properties file <br>
<code>vi /usr/local/kafka/config/server.properties</code><br>

<h3>server.properties configuration</h3>
Configure as desribed below<br>

The id of the broker. This must be set to a unique integer for each broker.<br>
<b>broker.id=0 </b><br>

increment this number for each node.
e.g. If you are on the first node broker.id=0,
if you’re on the second node broker.id=1 and so on. <br>

Zookeeper connection string (see zookeeper docs for details).
This is a comma separated host:port pairs, each corresponding to a zk
server. e.g. "127.0.0.1:3000,127.0.0.1:3001,127.0.0.1:3002".
You can also append an optional chroot string to the urls to specify the
root directory for all kafka znodes.
<b>zookeeper.connect=localhost:2181</b><br>

change this to a list of zookeeper node addresses with the zookeeper port:<br>
public_dns_1:2181,public_dns_1:2181,public_dns_1:2181<br>

Timeout in ms for connecting to zookeeper - can set to 6000

<h3>Setup JMX port </h3>
Setup JMX port in /usr/local/kafka/bin/kafka-server-start.sh <br>
<code>sudo nano /usr/local/kafka/bin/kafka-server-start.sh </code><br>

Add the following on the top of the file after all the comments<br>
<b>export JMX_PORT=${JMX_PORT:-9999}</b><br>

<h3>Start the Server</h3>
First start a zookeeper instance
<code>bin/zookeeper-server-start.sh config/zookeeper.properties</code>


Now start kafka server
<code>bin/kafka-server-start.sh config/server.properties</code>

<h3>Create a topic</h3>
Let's create a topic named "test" with a single partition and only one replica

<code>bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test</code>

We can now see that topic if we run the list topic command:<br>
<code>bin/kafka-topics.sh --list --bootstrap-server localhost:9092</code>

<h4>Send some Messages</h4>
Run the producer and then type a few messages into the console to send to the server
<code>bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test </code>
This is a message
This is another message

<h3>Setting up a multi-broker cluster</h3>
<code>cp config/server.properties config/server-1.properties</code>

<h3>Test out configuration</h3>
First create topic on one node
<code>/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-topic</code><br>

Then consume message on other nodes<br>
<code>/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-topic</code><br>

Now try to publish messages on another node<br>
<code>/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic </code><br>

Finally, go back to any node to view the message
<code>/usr/local/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-topic</code><br>

To list all topics run the following command from any node <br>
<code>bin/kafka-topics.sh --list --zookeeper localhost:2181</code><br>
