
<h1>Stock Expectations</h1>

<h3>Project Description</h3>
Current autoML tools (such as DataRobot and H2O serverless AI) have enabled faster model building and easier model deployment.
 Model maintenance (e.g. model retrain with new datasets) still remains a time-consuming task for Data Scientists. Especially as time goes by, the training data volume increase significantly, which poses a large data challenge for data ingestion and model retrain. Also the timing for model retain remains an open-ended question, should Data Scientists retrain model quarterly or whenever model deteriorates as customer provided feedback.
 In this project, an automatic model retrain framework is proposed, which will free up Data Scientist time for model performance monitoring and make it easier for Data Scientists to retrain model with large scale datasets.

 <h3>Engineering Challenge</h3>
 Construct pipeline to automate data extraction, data cleaning, feature engineering, and model training and to provide real time metrics feedback to Data Scientists.

 <h3>Business Case</h3>
 Using reddit comments datasets and the stack exchange datasets, build an automated model retraining framework when a new dataset is introduced to the machine learning model.

 <h3>Tech Stack</h3>
S3, Spark, Python, Redshift, Airflow

<h3>Datasets</h3>
Reddit Comments - http://academictorrents.com/details/85a5bd50e4c365f8df70240ffd4ecc7dec59912b
Stack Exchange - https://archive.org/details/stackexchange
