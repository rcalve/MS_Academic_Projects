USing Spark ML Library

Goals of the project:
- Perform Market Basket Analysis and Logistic Regression using Spark ML library
- Retreive the csv file from the DBFS and store in a Spark Dataframe
- Market Basket Analysis 
	- The goal of this task is to use Spark MLlib to build a model to generate association rules to quickly run the market basket analysis to uncover associations between different items, then further to provide recommendations for purchase on a distributed platform.
	- Import FPGrowth from Pyspark MLlib
	- Read the dataset stored in the DBFS on databricks
	- Modify the datatset to feed it into FPGrowth Model
	- Display the frequent itemsets, generated association rules for the train dataset and the model's predictions for the test dataset

- Logistic Regression 
	- The goal of this task is to build a machine learning pipeline including a classification model that predicts the `Attrition` (Yes or No) from the features included in the dataset (income, work years, education level, marital status, job role, and so on). 
	- Import the necessary libraries
	- Load the dataset from DBFS and display the schema
	- Split the dataset into train and test sets
	- Feature Processing
	- Defining the model and building a pipeline
	- Display the predictions & evaluate the model 
	- Hyperparameter tuning - Cross Validation
	- Running SQL commands on the final results



