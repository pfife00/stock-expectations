
<h3>Folder Structure</h3>

This directory contains the scripts to execute the preprocessing.py file located within the spark folder and the producer.py file located within the kafka folder.
To start the pipeline, first run the run.sh file by typing the following command to your terminal window:<br>
<code>sh run.sh</code><br>

To stop the process, run the stop.sh file by typing the following commad to your terminal window:<br>
<code>sh stop.sh</code><br>

Also located is the Dash application (app.py)<br>

<h3>Dash Installation</h3>

Dash can be installed using pip:<br>

<h3>Step 1: Install with Pip</h3><br>
Fist install the core dash backend<br>
<code>pip install dash==1.0.0</code><br>

Next install the  DAQ components <br>
<code>pip install dash-daq==0.1.0</code><br>

<h4>Version Check</h4><br>
To check which Dash version you are using <br>

First import the library<br>
<code>import dash_core_components</code><br>

Then run the print command<br>
<code>print(dash_core_components.__version__)</code><br>




```python

```
