#!/usr/bin/env python
# coding: utf-8

# # Course Section : AIT614-005
# ## Lab 2 : NoSQL MongoDB with Python
# ### Student's Name : Rashmika Calve

# In[1]:


get_ipython().system('pip install pymongo')


# #### Importing the required libraries

# In[2]:


import pymongo
import pandas as pd
import json


# #### Connect to MongoDB

# In[3]:


client = pymongo.MongoClient("mongodb://localhost:27017/")


# #### Load the csv file

# In[4]:


df = pd.read_csv("EmployeeAttrition.csv")
df.head(10)


# In[5]:


df.shape


# #### Converting the dataframe to JSON format and Loading to MongoDB

# In[6]:


# Converting the df to json 
emp_data = json.loads(df.to_json(orient='records'))


# #### Creating a Database

# In[7]:


mongo_db = client["myDB"]
mongo_db


# #### Creating a collection

# In[8]:


collection_nm = "Empl_Attrition"


# In[9]:


collection_nm = mongo_db[collection_nm]


# #### Insert the data into MongoDB Collection

# In[10]:


collection_nm.insert_many(emp_data)


# #### Query MongoDB

# ##### Count the total no of documents in the collection

# In[11]:


collection_nm.count_documents({})


# ##### 1. Count the no of employees whose TotalWorkingYears are greater than 20.

# In[12]:


collection_nm.count_documents({
    "TotalWorkingYears" : {"$gt" : 20}  })


# ##### 2. Find EmployeeNumber, EducationField, JobRole for all the employees whose Age is between 25 and 30 and Education is 5. Display only EmployeeNumber, EducationField, and JobRobe in the output.

# In[13]:


res = collection_nm.find({'Age' : {'$gte' : 25, '$lte' : 30},
                         "Education" : 5},
                         {'EmployeeNumber', 'EducationField','JobRole'}
                        )
print('EmployeeNumber', '\t', 'EducationField', '\t\t', 'JobRole')
print('--------------------------------------------------------')
for r in res:
    print(r['EmployeeNumber'], '\t\t', r['JobRole'], '\t\t', r['EducationField'])


# ##### 3. For all the women employees having Age between 35 and 40 and TotalWorkingYears < 5, sort EmployeeNumber in an ascending order. Print only Department and EmployeeNumber in the output.

# In[14]:


# Adding conditions to the find function
emp_res= collection_nm.find(
    {"$and": [
        {"Gender" : 'Female'},
        {'Age' : {'$gte' : 35}},
        {'Age' : {'$lte' : 40}},
        {'TotalWorkingYears' : {'$lt':5}}
    ]},
    {'EmployeeNumber','Department'}    
).sort('EmployeeNumber',1)


# In[15]:


# Converting the cursor to a list
emp_res_list = list(emp_res)


# In[16]:


# Converting the list to a dataframe
emp_df_3 = pd.DataFrame(emp_res_list)
emp_df_3.shape


# In[17]:


#Displaying the results
emp_df_3[['EmployeeNumber','Department']]


# ##### 4. Find employees whose HourlyRate is greater than or equal to 100 or DailyRate is greater than 1490. Display Age, HourlyRate, DailyRate, and Department only and sort DailyRate in an ascending order.

# In[18]:


# Adding conditions to the find function
emp_res4 = collection_nm.find(
    {'$or': [
        {'HourlyRate' : {'$gte':100}},
        {'DailyRate': {'$gt':1490}}
    ]},
    {'Age','HourlyRate','DailyRate','Department'}
).sort('DailyRate',1) # 1 means ascending order


# In[19]:


# Converting the cursor to a list
emp_res_list4 = list(emp_res4)
emp_res_list4


# In[20]:


# Converting the list to a dataframe
emp_df_4 = pd.DataFrame(emp_res_list4)
emp_df_4.shape


# In[21]:


#Displaying the results
emp_df_4.loc[ : , emp_df_4.columns != '_id']


# ##### 5. For each JobRole, find the average MonthlyIncome. Print out the formatted monthly incomes in hundredth and arrange them in descending order.

# In[22]:


emp_res5 = collection_nm.aggregate([
    {"$group": {
        "_id" : "$JobRole",
        "avg_monthly_income" : {"$avg" : '$MonthlyIncome'}
    }},
    {"$sort" : {
        "avg_monthly_income" : -1 }
    }
])


#Printing the results
print('Job Role', '\t\t\t\t', 'Average Monthly Income')
print('-----------------------------------------------------------------')
for r in emp_res5:
    print(f"{r['_id'] : <25}{'{:.2f}' : >30}".format(r['avg_monthly_income']))


# ##### 6. Count the different MaritalStatus when Attrition is YES and AGE is greater than 35 in the dataset. Arrange the count in descending order.

# In[23]:


emp_res6 = collection_nm.aggregate([
    {
        '$match' : {
            '$and': [
                {"Attrition":'Yes'},
                {'Age': {'$gt' : 35}}
            ]
        }
    },
    {
        "$group" : {
            "_id" : "$MaritalStatus",
            "count_emp" : {"$sum" : 1}
        }
    },
    {"$sort" : {
        "count_emp" : -1 }
    }
])


# In[24]:


list(emp_res6)


# ##### Delete All Documents in a Collection

# In[25]:


collection_del = collection_nm.delete_many({})


# ##### Delete the Collection

# In[26]:


collection_nm.drop()


# #### References

# ###### [1] Dr. Liao’s lab tutorials and code examples: Blackboard/Liao_PyMongo.html  
# ###### [2] Python MongoDB - https://www.w3schools.com/python/python_mongodb_getstarted.asp
# ###### [3] PyMongoDB Documentation - https://pymongo.readthedocs.io/en/stable/
