

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

<img width="1033" alt="Screen Shot 2019-07-04 at 14 09 12" src="https://user-images.githubusercontent.com/17607212/60687749-67b03f00-9e65-11e9-96b0-3208189275a8.png">


 <h3>Engineering Challenge</h3>
Employing Great Expectations in a streaming environment proved to be a challenging task as it does not currently support a streaming environment. To overcome this challenge, several data processing steps within spark had to be performed in order utilize Great Expectations. 


 <h3>Tech Stack</h3>
S3, Kafka, Spark, Great Expectations, PostgreSQL, Dash<br>


![StockExpectations (1)](https://user-images.githubusercontent.com/17607212/60687570-2d926d80-9e64-11e9-82f7-05a18168d314.jpg)







<h3>Datasets</h3>
The Deutsche Börse Public Dataset is a near real-time streaming stock data dataset stored in an external S3 bucket. The data dictionary for the data can be viewed in the dataset's <a href="https://github.com/Deutsche-Boerse/dbg-pds">Github repo</a>.<br>
<h3>Data Dictionary</h3>

The Xetra data is an S3 bucket stored at the following location:<br>
s3://deutsche-boerse-xetra-pds <br>

Each Xetra csv file within the bucket is defined as follows<br>
<ul>
    <li><b>ISIN</b> ISIN of the security:	string</li>
    <li><b>Mnemonic</b>	Stock exchange ticker symbol:	string</li>
<li><b>SecurityDesc</b>	Description of the security:	string</li>
<li><b>SecurityType</b>	Type of security:	string</li>
<li><b>Currency</b>	Currency in which the product is traded	ISO 4217: string (see https://en.wikipedia.org/wiki/ISO_4217)</li>
<li><b>SecurityID</b>	Unique identifier for each contract:	int</li>
<li><b>Date</b>	Date of trading period:	date</li>
<li><b>Time</b>	Minute of trading to which this entry relates:	time (hh:mm)</li>
<li><b>StartPrice</b>	Trading price at the start of period:	float</li>
<li><b>MaxPrice</b>	Maximum price over the period:	float</li>
<li><b>MinPrice</b>	Minimum price over the period:	float</li>
<li><b>EndPrice</b>	Trading price at the end of the period:	float</li>
<li><b>TradedVolume</b>	Total value traded:	float</li>
<li><b>NumberOfTrades</b>	Number of distinct trades during the period:	int</li>
</ul>
The Deutsche Börse Public Dataset (DBG PDS) S3 bucket is available from <a href="http://s3://deutsche-boerse-xetra-pds">here</a>.
