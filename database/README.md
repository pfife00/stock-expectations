<h2>PostgreSQL Installation</h2>
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
