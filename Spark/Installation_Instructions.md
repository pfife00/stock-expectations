
<h3>Step 0 - Configure Cluster System </h3>
    <ul>
    <li>First setup a 4 node cluster called spark-cluster using 4 m4.large ec2 instances.</li>
    <li>Next configure each node following instructions to setup and configure java and passwordless SSH between each node</li>
</ul>
<h3>Step 1 - Install Scala on each node </h3>
<code>sudo apt install scala</code><br>
<code>scala -version</code>
Make node of scala version:
Scala code runner version 2.11.12 -- Copyright 2002-2017, LAMP/EPFL
<h3>Step 2: Installing Spark</h3>
<ul>
<li>On each machine (both master and worker) install Spark using the following commands. You can configure your version by visiting https://spark.apache.org/downloads.html<br>
<code>wget http://apache.claz.org/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz</code><br></li>
<li>Extract the files and move them to /usr/local/spark and add the spark/bin into PATH variable.</li>
<code>tar xvf spark-2.4.3-bin-hadoop2.7.tgz</code><br>
<code>sudo mv spark-2.4.3-bin-hadoop2.7/ /usr/local/spark</code><br>
<code>vi ~/.bash_profile</code><br>
export PATH=/usr/local/spark/bin:$PATH<br>
<code>source ~/.bash_profile </code>
</ul>
<h3>Step 3: Configuring Master to keep track of its workers</h3>
<ul>
<li>Modify /usr/local/spark/conf/spark-env.sh file by providing information about Java location and the master node’s IP.<br>
contents of conf/spark-env.sh</li>
<code>export SPARK_MASTER_HOST=master-private-ip</code><br>
<code>export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/</code><br>
Note: If the spark-env.sh doesn’t exist copy the spark-env.sh.template and rename it.<br>

<li>Add all the IPs where the worker will be started. Open the /usr/local/spark/conf/slaves file and paste the following.<br>
contents of conf/slaves
<li>worker1 private IP</li>
<li>worker2 private IP</li>
<li>worker3 private IP</li></li>
</ul>

<h3>Step 4: Set oversubscription</h3>
Set the SPARK_WORKER_CORES flag in spark-env.sh to a value higher than the actual number of cores.
Example: If each of our three workers have 2 cores, we have total of 6 cores available. We can set the WORKER_CORES to be 3 times that to allow for oversubscription.<br>
<code>export SPARK_WORKER_CORES=6</code>

<h3>Step 5: Test Configuration</h3>
Run script and it starts it as a background process so you can exit the terminal.
<code>sh /usr/local/spark/sbin/start-all.sh</code><br>
Once you want to stop the service you can run<br>
<code>sbin/stop-all.sh</code>

<h3>Can use Pegasus to Install Spark as well</h3>
Follow steps in Pegasus documentation to install Spark with Pegasus if prefer that route



```python

```
