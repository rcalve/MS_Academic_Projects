#!/usr/bin/env python
# coding: utf-8

# <h1> Task 1 - Market Basket Analysis and Product Recommendation  </h1>
# 
# <h6> GOAL: The goal of this task is to use Spark MLlib to build a model to generate association rules to quickly run the market basket analysis to uncover associations between different items, then further to provide recommendations for purchase on a distributed platform.   </h6>

# In[ ]:


# Importing the library
from pyspark.ml.fpm import FPGrowth


# In[ ]:


# 1.3 - Creating the training set
# Reading the dataframe
train_df = spark.read.format("csv").option("header", "false").load("dbfs:/FileStore/shared_uploads/clvrashmika@gmail.com/Lab5_Part1_TrainData.csv")


# In[ ]:


# Displaying the dataframe
display(train_df)


# In[ ]:


# Modifying the dataframe to perform analysis
count = 0
mylist = []
for row in train_df.collect():
    temp = (count,list(filter(None, row)))
    mylist.append(temp)
    count = count + 1


# In[ ]:


# Printing the list to show the new format
mylist


# In[ ]:


# Creating a new dataframe from the above list
train_df1 = spark.createDataFrame(mylist, ["id", "items"])


# In[ ]:


# 1.4 - FP Growth Model
fpGrowth = FPGrowth(itemsCol="items", minSupport=0.05, minConfidence=0.07)
model = fpGrowth.fit(train_df1)


# In[ ]:


#1.5 -  Display frequent itemsets.
model.freqItemsets.show()


# In[ ]:


#1.6  Display generated association rules.
display(model.associationRules)


# In[ ]:


# 1.7 Creating a test set
test_df = spark.createDataFrame([
    (0, ['bread']),
    (1, ['potatoes','milk']),
    (2, ['chocolate']),
    (3, ['pasta', 'cheese']),
    (4, ['apple','milk']),
    (5, ['milk']),
    (6, ['chocolate', 'bread', 'milk']),
    (7, ['bread', 'milk'])
], ["id", "items"])


# In[ ]:


# 1.8 Making predictions
# transform examines the input items against all the association rules and summarize the consequents as prediction
display(model.transform(test_df))


# #####  1.10 Task 1 - Additional

# In[ ]:


# Reading and displaying the dataframe
extra_df = spark.read.format("csv").option("header", "false").load("dbfs:/FileStore/shared_uploads/clvrashmika@gmail.com/groceries.csv")
display(extra_df)


# In[ ]:


# Modifying the dataframe to perform analysis
count = 0
mylist = []
for row in extra_df.collect():
    temp = (count,list(filter(None, row)))
    mylist.append(temp)
    count = count + 1
    
# Creating a new dataframe from the above list
extra_df1 = spark.createDataFrame(mylist, ["id", "items"])


# In[ ]:


# Splitting the dataset into train and test dataframes
trainDF, testDF = extra_df1.randomSplit([0.8, 0.2], seed=25)
print(trainDF.cache().count()) # Cache because accessing training data multiple times
print(testDF.count())


# In[ ]:


# FP Growth Model
fpGrowth = FPGrowth(itemsCol="items", minSupport=0.01, minConfidence=0.01)
model = fpGrowth.fit(trainDF)


# In[ ]:


# Display frequent itemsets.
display(model.freqItemsets)


# In[ ]:


# Display generated association rules.
display(model.associationRules)


# In[ ]:


# transform examines the input items against all the association rules and summarize the
# consequents as prediction
display(model.transform(testDF))


# <h3> 1.9 References: </h3>
# 
# <p>
#   <b>1.</b>  Dr. Liao’s Code Examples & Tutorials: Blackboard/Liao_PySpark_basic_databricks.html
#   <br>
#   <b>2.</b> PySpark: https://spark.apache.org/docs/2.4.0/api/python/pyspark.html  
#   <br>
#   <b>3.</b> Frequent Pattern Mining : https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html
# </p>
