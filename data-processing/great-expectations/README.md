
<h2>Great Expectations</h2>
Great expectations provides an approach to automated testing: pipeline tests. Pipeline tests are applied to data (instead of code) and at batch time (instead of compile or deploy time). Pipeline tests are like unit tests for datasets: they help you guard against upstream data changes and monitor data quality. <a href="http://docs.greatexpectations.io/en/latest/index.html#/">Great Expectations Documentation</a><br>


<h3>Installation</h3>
The Great Expectations library requires a python version greater than 3.5. To install on ubuntu 16.04 version, you have to install the a python version higher than 3.5. I installed python 3.7 for this project.

<h4>Step 1: Install Anaconda Environment</h4>
To properly install Great Expectations after installing python is to install the Anaconda environment.
First download the Anaconda package: <br>
<code>wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh</code><br>

Next run the installer:<br>
<code>sh Anaconda3-2019.03-Linux-x86_64.sh</code><br>

<h4>Step 2: Setup the Anaconda Environment</h4>
Activate the installation by running<br>
<code>source ~/.bashrc</code><br>

<h4>Step 3: Install Great Expectations</h4>
Install the library by running:<br>
<code>pip install great-expectations</code><br>
