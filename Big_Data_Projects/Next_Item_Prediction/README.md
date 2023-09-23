# Abstract

Compiling a grocery list and ensuring everything is on the list is a time consuming process.  This analysis is intended to provide a real time analysis of the items selected in a person's cart and make suggestions for the next item based on what items are currently in the cart.  There were two main objectives of this analysis.  The first objective was to make recommendations based on the data for all users. The second was to make recommendations on individual user selections. 

A data set was found that was used in a Kaggle competition.  This dataset was chosen due to the interesting outcomes that can be achieved & also its size which supported the need for Big Data tools.  While the number of orders was large totalling  to 3.42 million, the primary data file, which provided a relationship between the orders and the products in an order contained 33.8 million records.  

The analysis was performed on a combination of platforms but key components were MongoDB, DataBricks, PySpark and SparkML.  Data from the dataset was provided in CSV format.  These CSV files were loaded into an MongoDB hosted on, mongoDBs own platform Atlas.  The data was used across the analysis methods.  The analysis was then executed from the mongDB into Databricks where it was processed using a combination of PySpark and Spark Machine Learning libraries.   

In order to meet the goals of the analysis, four different analysis methods were used; decision tree analysis, Apriori analysis, Collaborative filtering and customer segmentation. (Team Project). My contribution to the team was the Collaborative Filtering Approach. 

The Apriori analysis used the FPGrowth Algorithm.  While this method produced results, the lift and confidence values were low.  Executing on DataBricks but took 2 hours for each run.  Individual user analysis was performed but the results were overly simplistic as many users had very little data. 

The collaborative filtering approach was implemented using the ALS algorithm in Pyspark (Apache Spark. (n.d.)) Collaborative filtering matches users with similar preferences and provides recommendations for each user. The size of the dataset made it quite a challenge to execute the model. Our model provides the top 3 recommendations for each user and each item.

Overall the results of  the analysis did allow us to exercise and struggle with a large data set and the solutions to dealing with large data sets.  While this is a large dataset to be used in an educational setting, it is small compared to industry datasets. The analysis produced mixed results with each analysis method producing results but with some caveats.  Future work should focus on novel ways to segment the problem space.  Using aisles or product groups may be an interesting way to segment the problem space and produce more focused results. 

# COLLABORATIVE FILTERING APPROACH:

The collaborative filtering approach was executed to come up with recommendations keeping the user’s past purchases in mind. This approach also takes into account similar patterns of other users to provide recommendations. At the end of this approach, we obtained two sets of recommendations - Top 3 product recommendations for each user and top 3 users for whom a certain product can be recommended.

To understand how collaborative filtering works, the initial attempt was to use the ‘pyasrule’ package in python to make the next item predictions using cosine similarity. Only a part of the dataset was used to execute this approach. Once we understood the results, we proceeded to look up ways to execute the collaborative filtering approach in PySpark.

PySpark uses the Alternation Least Squares Method (ALS) to perform the collaborative filtering approach. In order to implement this model, we would require the user ID, the product ID of the purchased product and the number of times each product was purchased. The user ID column is used to for the userCol input of the model, the product ID is used for the itemCol input of the model and the number of times each product is purchased is used for the rating input of the model since we do not have an actual rating in this case.

Pre-processing the entire dataset was one of the biggest challenges here. For the initial pre-processing, we had to combine the order_products__train (1.4M records), order_products__prior (32.4M records) and products file to get a combination of the user_id, product_id and the number of times each product was purchased. All the required files were read as pyspark dataframes from mongodb in databricks. Order_products__prior and order_products__train were merged to get the user_id and order_id. This was later merged with ‘products’ dataframe to extract the product_id.

This pre-processed dataframe was given as the input to the ALS model. The ALS model predicts two sets of recommendations.
I) Top 3 product recommendations for each user
II) Top 3 users for whom a product can be recommended.

We chose to stick to only the top 3 recommendations owing to the large size of the dataset.

Overall, this approach was effective in terms of considering a user’s past purchases and also comparing them to other users with similar patterns. Another advantage of using this approach was to come up with product recommendations that may not have occurred in the training dataset. For example, if the training dataset did not see a combination of Eggs and Bread, the Apriori algorithm might not predict this but the collaborative filtering approach will provide this recommendation if it sees users with similar patterns and there is a high chance of them purchasing the product.



# Execution Environment 
The analysis was performed on DataBricks.  In order to run the ipynb files, the DataBricks cluster must be configured with pymongo, mongo-spark-connector_2.12:3.0.1 and networkx.  The following is instructions to install these items. 

## Create and Configure Cluster
1. Create a Cluster 
2. Go to Cluster->Configuration -> libraries
3. Click Install New 
4. Click pypl
5. Respository = pymongo
6. Click install
7. On the libraries tab
8. Click Install new
9. Click Maven
10. Click Search Packages
11. Type mongo into the search box
12. Select org.mongodb.spark:mongo-spark-connector_2.12:3.0.1
13. Click Install
14. On the libraries tab
15. Click Install new 
16. Click pypl
17. Repository   = networkx
18. Click Install


# Instructions to run the file:

The entire code can be easily run on the Databricks platform. 
1)	Download the python notebook named AIT_614_Group_3_Final_Project _Collaborative_Filtering.ipynb
2)	Create a cluster with the databricks runtime version as - 13.0 ML (includes Apache Spark 3.4.0, Scala 2.12)  and 15GB Memory. 
3)	Once the cluster is created, go to the Libraries tab on the cluster details page and upload the following libraries :
  a)	Select the Install New Option → Library Source as PyPI → Package name as pymongo → Install
  b)	Select the Install New Option → Library Source as Maven → Click the Search Packages option → Search for org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 → Install
4)	Once the above packages have been installed, create a new notebook in Databricks
5)	Once the notebook has been created, select File → Import Notebook → Choose the python notebook AIT_614_Group_3_Final_Project _Collaborative_Filtering.ipynb
6)	The entire python code is now uploaded to the created notebook. 
7)	Connect this notebook to the created cluster. You are now ready to run the code.
8)	You can select the ‘Run All’ option from the ‘Run’ Menu to run the entire code at once. It might take a while to run the file as some commands take longer to run due the large size of the dataset. 



Apache Spark. (n.d.). Collaborative Filtering - Spark 3.4.0 Documentation. Apache Spark. Retrieved April 29, 2023, from https://spark.apache.org/docs/latest/ml-collaborative-filtering.html
