
<h2>DIRECTORY DESCRIPTION</h2>

This folder contains 2 subfolders: <br>
<ul>
    <li>spark - contains preprocessing.py file, master and worker yml files and an installation instructions readme</li>
    <li>great-expectations - contains a readme file on how to install the great expectations library</li>
</ul>

<h4>pyspark installation</h4>
<code>pip --no-cache-dir install pyspark</code>

<h4>preprocessing.py</h4>
The preprocessing.py file should be located within the /home/ubuntu directory

<h4>Setting Python to Version 3.5</h4>
In order to utilize the Great Expectations library, Python version 3.6 or higher is required. Ubuntu 16.04 ships default with Python 3.5 by default. The spark workers were upgraded to Python 3.5 in order to communicate with the spark master which is running Python 3.7.<br>
Setting the default version on each node requires the following code blocks:
<code>sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1</code><br>
<code>sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2</code><br>
<code>sudo update-alternatives --config python</code><br>
Choose option 2 after running the third code block<br>

On the spark-master node, and additional step is required by changing the following value:
<code>vi ~/.bashrc</code><br>
change the variable <code>alias python='/usr/bin/python3.6</code><br> to which python you wish to use.<br>

then run:
<code>source ~/.bashrc</code><br>
