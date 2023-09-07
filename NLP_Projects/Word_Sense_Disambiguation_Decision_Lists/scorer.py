import sys
from bs4 import BeautifulSoup
import logging

# Creating the logger and configuring it
logging.basicConfig(filename="decision_list_log.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object for logger
logger = logging.getLogger()

# Setting the threshold of logger to DEUBG
logger.setLevel(logging.INFO)

# Reading the values from the terminal
my_answers_file = open(sys.argv[1])
actual_answers_file = open(sys.argv[2])


# Function to read the input file, parse it and return a dictionary
# The key is the ID
# Value is the senseid
def read_file_for_me(inputfilename):
    Lines = inputfilename.readlines()
    answers = {}
    for line in Lines:
        soup=BeautifulSoup(line, features ='lxml')
        # Finding the text for answer
        val=soup.find('answer')
        # storing the instance id as the key
        key_data = val.get('instance')
        # storing the senseid as the value
        value_data = val.get('senseid')
        # adding them to the dictionary
        answers[key_data] = value_data

    logger.info("Completed reading file and creating a dictionary")
    return answers

my_answers_dict = read_file_for_me(my_answers_file)
actual_answers_dict = read_file_for_me(actual_answers_file)

#print(my_answers_dict)
#print('Now see the actual one: \n')
#print(actual_answers_dict)

count = 0
tp = 0
tn = 0
fp = 0
fn = 0

for i in my_answers_dict:
    if my_answers_dict[i] == actual_answers_dict[i]:
        count += 1
    if my_answers_dict[i] == 'phone' and actual_answers_dict[i] == 'phone':
        tp += 1
    if my_answers_dict[i] == 'phone' and actual_answers_dict[i] == 'product':
        fp += 1
    if my_answers_dict[i] == 'product' and actual_answers_dict[i] == 'phone':
        fn += 1
    if my_answers_dict[i] == 'product' and actual_answers_dict[i] == 'product':
        tn += 1

# Calculating the accuracy and confusion matrix
print('TP', tp) # True Positive
print('FP', fp) # False Positive
print('FN', fn) # False Negative
print('TN', tn) # True Negative

# Adding the true positive and true negative values to get the accuracy
Accuracy = ((tp + tn) / len(my_answers_dict))
print('Accuracy -', Accuracy * 100, '%')

# Creating a 2D array to store the confusion matrix values
rows, cols = 2, 2

# Creating the matrix & Assigning all the values to zero
confusion_matrix = [[0] * cols] * rows

confusion_matrix = [[tp, fp], [fn, tn]]

print('Confusion Matrix: ', confusion_matrix)

logger.info('All steps completed successfully')
