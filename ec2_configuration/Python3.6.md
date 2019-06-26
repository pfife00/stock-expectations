
<h2>Set Python3.6</h2>

In order to use the Great Expectations library, each node should have Python3.6 set as default Python version. Since Python3.6 is not included by default in Ubuntu version 16.04, then Python must be downloaded and installed<br>

<h3>Step 1: Download Python</h3>
Following the instructions in this <a href="https://medium.com/@moreless/install-python-3-6-on-ubuntu-16-04-28791d5c2167/">Medium</a> article, install from PPA (Method 2).

Install the following requirements<br>
<code>apt-get install software-properties-common python-software-properties</code><br>

Run the following command to add the PPA<br>
<code>add-apt-repository ppa:jonathonf/python-3.6</code><br>

<h4>Update the Repositories</h4>
<code>apt-get update</code><br>

<h3>Step 2: Install Python 3.6</h3>
<code>apt-get install python3.6</code><br>

<h3>Step 3: Change default to Python 3.6</h3>
First the command should give an error

<code>sudo update-alternatives --config python</code><br>

update-alternatives: error: no alternatives for python3<br>

Need to update your update-alternatives to set default python version<br>
<code>sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 1</code><br>
<code>sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2</code><br>

Then run below to python3.6 as default. Choose the option which corresponds to the Python3.6 choice.<br>
<code>sudo update-alternatives --config python</code><br>
