

<h1>Stock Expectations: Anomaly detection using Great Expectations</h1>

![StockExpectations](https://user-images.githubusercontent.com/17607212/60687481-b52bac80-9e63-11e9-8b01-775a46686e66.jpg)


<h3>Project Description</h3>
There is an inherent belief in the stock mark that the price of stocks should fully
reflect all available data. However, what if that data is flawed? What if there are 
anomalies in the data?<br> 
How do we go about finding these anomolies?<br>


<h4>Great Expectations</h4>
To help answer this question, I employed the Great Expectations library which applies "expectations" to the data pipeline in order look for data which does not meet those expectations. An example expectation that is applied to the pipeline is provided below.
<code>sdf.expect_column_max_to_be_between("MAX_PRICE", 1, 500, result_format="BOOLEAN_ONLY")</code><br>
This expectation applies the expecation to the data that the maxiumum price should not be greater than 500 or less than 1. If that expectation is not met, then the user is provided a flag (see dashboard image) to take appropriate action.

 <h3>Engineering Challenge</h3>
Employing Great Expectations in a streaming environment proved to be a challenging task as it does not currently support a streaming environment. To overcome this challenge, several data processing steps within spark had to be performed in order utilize Great Expectations. 


 <h3>Tech Stack</h3>
S3, Kafka, Spark, Great Expectations, PostgreSQL, Dash
![StockExpectations (1)](https://user-images.githubusercontent.com/17607212/60687537-edcb8600-9e63-11e9-8fa3-73b6f1f4607d.jpg)

<h3>Datasets</h3>
The Deutsche Börse Public Dataset is a near real-time streaming stock data dataset stored in an external S3 bucket. The data dictionary for the data can be viewed in the dataset's <a href="https://github.com/Deutsche-Boerse/dbg-pds">Github repo</a>.<br>
The Deutsche Börse Public Dataset (DBG PDS) S3 bucket is available from <a href="http://s3://deutsche-boerse-xetra-pds">here</a>.




```python

```
