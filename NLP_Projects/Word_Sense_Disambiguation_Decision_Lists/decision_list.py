# Importing the neccessary libraries
from bs4 import BeautifulSoup  # for reading xml files
from nltk.tokenize import word_tokenize # for tokenizing
from nltk.probability import ConditionalFreqDist  # to calculate probabilities for the decision list
import string
import re
from nltk.corpus import stopwords
from nltk.probability import ConditionalProbDist, ELEProbDist
import operator
from pattern.text.en import singularize # to remove plurals
import sys # to read the input from the terminal
import logging

# Reading the inputs from the terminal
train_xml_file_loc = sys.argv[1]
test_xml_file_loc = sys.argv[2]
output_text_file = sys.argv[3]

# Creating the logger and configuring it
logging.basicConfig(filename=output_text_file,
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object for logger
logger = logging.getLogger()

# Setting the threshold of logger 
logger.setLevel(logging.INFO)

# To clean the input file
# Here, we perform the following
# 1) tokenize the text into words
# 2) remove plurals
# 3) remove punctuations
# 4) remove stop words
def data_cleaning(input_data):
    tokenized_data = word_tokenize(input_data)
    singularized_data = [singularize(token) for token in tokenized_data]
    without_punct = [''.join(
        eachcharac for eachcharac in eachword if eachcharac not in string.punctuation and not eachcharac.isdigit()) for
                     eachword in singularized_data]
    final_words_without_punct = [eachw.lower() for eachw in without_punct if eachw != '']

    stop_words = set(stopwords.words('english'))
    without_stop_words = []

    for i in final_words_without_punct:
        if i not in stop_words:
            without_stop_words.append(i)

    return without_stop_words


# Read the xml file (only train) and create a list of dictionaries containing the id, senseid & tokenized string
# for that id
def read_xml_train(file_name):
    temp=[] # to create a list of dictionaries
    file = open(file_name, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'xml')
    instances = soup.find_all('instance') # getting all the instance tags
    for data in instances:
        temp.append(
        {
        'id':data.answer.get('instance'),
        'senseid':data.answer.get('senseid'),
        'tokenized_string': data_cleaning(data.get_text().strip().lower())
            # here we are converting the text to lower case & sending it to data cleaning
        }
        )
    logger.info("Completed reading and cleaning the training data")
    return temp


# Very similar to the read_xml_train function
# Only difference is that this does not have the senseid
# This also returns a list of dictionaries
def read_xml_test(file_name):
    temp=[]
    file = open(file_name, "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'xml')
    instances = soup.find_all('instance')
    for data in instances:
        temp.append(
        {
        'id':data.get('id'),
        'tokenized_string': data_cleaning(data.get_text().strip().lower())
        }
        )
    logger.info("Completed reading and cleaning the test data")
    return temp


# To calculate the conditional frequency, probability and form the decision list from the derived features
def build_decision_list(input_array):
    decision_list = []
    cfdist = ConditionalFreqDist()
    for i in input_array:
        for k in range(len(i['tokenized_string'])):
            # if the word line or lines is present in the centre where it can read the k-2, k-1 and kth word
            # Example A B line C
            if ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][
                k] == 'lines') and k != 0 and k != 1 and k != len(i['tokenized_string']) - 1):
                cfdist[str(i['tokenized_string'][k - 2]) + '_line'][i['senseid']] += 1
                cfdist[str(i['tokenized_string'][k - 1]) + '_line'][i['senseid']] += 1
                cfdist['line_' + str(i['tokenized_string'][k + 1])][i['senseid']] += 1

            # if the word line or lines is the first word
            # for example: line A
            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == 0 and k != len(
                    i['tokenized_string']) - 1):
                cfdist['line_' + str(i['tokenized_string'][k + 1])][i['senseid']] += 1

            # if the word line or lines is the second word
            # for example A line B
            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == 1 and k != len(
                    i['tokenized_string']) - 1):
                cfdist[str(i['tokenized_string'][k - 1]) + '_line'][i['senseid']] += 1
                cfdist['line_' + str(i['tokenized_string'][k + 1])][i['senseid']] += 1

            # if the word line or lines is the last word
            # for example: A B line
            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == len(
                    i['tokenized_string']) - 1):
                cfdist[str(i['tokenized_string'][k - 2]) + '_line'][i['senseid']] += 1
                cfdist[str(i['tokenized_string'][k - 1]) + '_line'][i['senseid']] += 1

            # print(cfdist.items())

    # to calculate the conditional probability distribution for the decision tree
    cond_cfdist = ConditionalProbDist(cfdist, ELEProbDist, 10)

    #Building the Decision List for phone and product for each feature
    for feature in cond_cfdist.conditions():
        decision_list.append(
            {
                'senseid': 'phone',
                'feature': feature,
                'probability': cond_cfdist[feature].prob('phone')
            }
        )
        decision_list.append(
            {
                'senseid': 'product',
                'feature': feature,
                'probability': cond_cfdist[feature].prob('product')
            }
        )

    # sorting the list in descending order as per the probability
    decision_list.sort(key=operator.itemgetter('probability'), reverse=True)

    # for i in decision_list:
    #     print(i)
    logger.info("Decision Tree Built is:")
    temp_str=""
    for i in decision_list:
        temp_str=temp_str+str(i['senseid'])+"\t--\t"+str(i['feature'])+"\t--\t"+str(i['probability'])+"\n"
    logger.info("decision list is:\n"+temp_str)
    return decision_list


# Deriving the collocations for the test data
# Same conditions as the train data
# Difference - we add the values to a list of dictionaries here
def get_collocations(cleaned_test_array, decision_list):
    res = []
    count = 0
    for i in cleaned_test_array:
        count = count + 1
        for k in range(len(i['tokenized_string'])):
            if ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][
                k] == 'lines') and k != 0 and k != 1 and k != len(i['tokenized_string']) - 1):
                # print("generic",count," ",i)
                res.append(
                    {

                        'id': i['id'],
                        'collocations': list((str(i['tokenized_string'][k - 2]) + "_line",
                                              str(i['tokenized_string'][k - 1]) + "_line",
                                              "line_" + str(i['tokenized_string'][k + 1]))),
                        'senseid_result': 'none'

                    })
                break;

            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == 0 and k != len(
                    i['tokenized_string']) - 1):
                # print("0 case",count," ",i)
                res.append(
                    {
                        'id': i['id'],
                        'collocations': list(("line_" + str(i['tokenized_string'][k + 1]))),
                        'senseid_result': 'none'

                    })
                break;


            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == 1 and k != len(
                    i['tokenized_string']) - 1):
                # print("1 case",count," ",i)
                res.append(
                    {
                        'id': i['id'],
                        'collocations': list((str(i['tokenized_string'][k - 1]) + "_line",
                                              "line_" + str(i['tokenized_string'][k + 1]))),
                        'senseid_result': 'none'

                    })
                break;

            elif ((i['tokenized_string'][k] == 'line' or i['tokenized_string'][k] == 'lines') and k == len(
                    i['tokenized_string']) - 1):
                # print("complete len",count," ",i)
                res.append(
                    {
                        'id': i['id'],
                        'collocations': list((str(i['tokenized_string'][k - 2]) + "_line",
                                              str(i['tokenized_string'][k - 1]) + "_line")),
                        'senseid_result': 'none'

                    })
                break;

    # for each feature, we check the probability scores from the decision list and take the highest one
    for i in range(len(res)):
        # print(res[i]['collocations'], res[i]['senseid_result'])
        dummy_list = []
        for each_element in decision_list:
            if each_element['feature'] in res[i]['collocations']:
                dummy_list.append(each_element)

        # sorting to get the top result
        dummy_list.sort(key=operator.itemgetter('probability'), reverse=True)

        # If there is no match then a default option - product will be returned
        if (len(dummy_list) == 0):
            res[i]['senseid_result'] = 'product'
            # print(res[i]['id'],res[i]['collocations'], 'default - product')

        # If there is a match with the decision list it returns the senseid
        else:
            res[i]['senseid_result'] = dummy_list[0]['senseid']
            # print(dummy_list[0]['senseid'])

    #print(len(res))
    logger.info("Created collocations, match with decision list and got results for test data")
    return res

# Intializing array to for train and test data
logger.info("Starting now")
train_data_cleaned = []
test_data_cleaned = []



logger.info("Read file names from the console")

# train_xml_file_loc = "C:\\Users\\RASHMIKA\\Documents\\GMASON WORK\\SEM 2\\AIT526 - NLP\\Course_Material\\Assignments\\line-data(2)(1)\\line-data\\line-train.xml"
# test_xml_file_loc = "C:\\Users\\RASHMIKA\\Documents\\GMASON WORK\\SEM 2\\AIT526 - NLP\\Course_Material\\Assignments\\line-data(2)(1)\\line-data\\line-test.xml"

# Calling the functions for train data
logger.info("Calling the functions to process the train data")
train_data_cleaned = read_xml_train(train_xml_file_loc)
decision_list_train = build_decision_list(train_data_cleaned)


# Calling the functions for test data
logger.info("Calling the functions to process the test data")
test_data_cleaned = read_xml_test(test_xml_file_loc)
test_colloc = get_collocations(test_data_cleaned, decision_list_train)

# Creating a dictionary with key as the id and value as the senseid result for the test data predictions
predicted_answers = {}
for i in range(len(test_colloc)):
    key_data = test_colloc[i]['id']
    value_data = test_colloc[i]['senseid_result']
    predicted_answers[key_data] = value_data
    # Printing to the console so that it gets stored in a file
    print(f'<answer instance="{key_data}" senseid="{value_data}" />')
logger.info("Stored results to a text file")
