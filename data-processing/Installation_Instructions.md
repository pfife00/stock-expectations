
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


<h3>PostgreSQL Installation</h3>
PostgreSQL was installed on an m5.large ec2 instance following the blog instructions written by Sriram Baskaran <a href="https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252/">Simply Install: PostgreSQL</a><br>
<h4>Step 1 Installation</h4>
First run the following commands to download and install PostgreSQL on the m5.large node. Note, that I will refer to the node as cache from this point forward.<br>
<code>ubuntu@ip-10-0-0-13:$ sudo apt update</code><br>
<code>ubuntu@ip-10-0-0-13:$ sudo apt install postgresql postgresql-contrib</code><br>

PostgreSQL can be started, stopped, restarted, etc:
<code>sudo service postgresql </code><br>
<code>[start|stop|restart|status]</code><br>

PostgreSQL is set up as a peer authentication, which means it uses client OS’s user profile to authenticate the user.

First log into postgres user
<code>sudo -u postgres -i</code><br>

Use psql to access PostgreSQL commannd line interface. <br>

<h4>Step 2 Modify Configuration files</h4>
First modify postgresql.conf at the following path:
<code>/usr/local/etc/postgresql/10/main</code><br>

As a best practice, the port number should be changed and changes to port and max_connections require a restart (using the service command).<br>
Set the listen address value to * <br>
listen_addresses = '*' <br>

Modify the pg_hba.conf file by adding:
host    database      user      0.0.0.0/0        md5 <br>

As a best practice, specify a database, user and a source IP.

<h4>Step 3 Create a new user with a password for application access</h4>
<code>postgres=# CREATE USER db_select WITH PASSWORD '<setpassword>';</code><br>
