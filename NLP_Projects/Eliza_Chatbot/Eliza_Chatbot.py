# Objective : The main objective of this assignment is to build a chatbot that plays the role of a psychotherapist,
#             similar to the working of Eliza.
#             This code will showcase the implementation of using regular expressions, word spotting, sentence
#             formation and various other functions that help in capturing text and generating appropriate responses.

# Team Members :
# 1. Anika Binte Islam
# 2. Rashmika Calve

# Examples : Our chatbot starts off by introducing itself and asking for the user's name.
#             Here is a sample of the same.
#             Eliza  : Hi, I'm Eliza, your e-psychotherapist! What is your name?
#             User   : My name is ABC
#             Eliza  : Hi ABC, How can I help you today ?


# Points to remember while using our Chatbot
#    1.  The chatbot that we have built is currently running with only minimal set of responses. We have around 18
#        responses that our chatbot is currently able to recognize and respond back.
#    2.  For responses that the chatbot is unable to recognize or does not have a predefined response in the dictionary,
#        it returns a set of default responses -
#        --  "I am unable to understand,can you tell me little bit more?",
#        --  "I didn't quite understand that. Can you say it in another way ?"
#    3.  When asked for your name, please respond back in one of the following ways :
#          a) My name is ABC
#          b) I am ABC
#          c) I'm ABC
#          d) ABC
#

# How does our chatbot work ?
#   1. The chatbot initially asks for the user's name and extracts it from the response.
#   2. All the following responses will have the user's name to the left to know whose response it is.
#   3. Post the extraction of the name, based on the user's input, our program searches through the predefined
#      dictionary that has a set of regular expressions as the keys and some predefined responses as a list
#      in the values.
#      If a match is found, then it picks a random response from the set of predefined values.
#   4. It is then passed through a dictionary to change the pronouns. Eg) me is changed to you
#   5. One of the goals of this assignment is to extract parts of the question and use it in the response. We have
#      accomplished this using {} in the predefined responses. Places where {} are found are the places where parts
#      extracted from the users response are used in Eliza's response.
#       For example, the user says - i am sad
#       Eliza's response would be - Why are you sad ?
#   6. When Eliza is unable to recognize the user's question/response, a default answer will be returned.
#   7. Words like bye, Bye, quit and Quit are used to end the conversation with the user.

# Implementation Code
import re      # for regular expressions
import random  # to pick a random response from the list of values in the dictionary
import sys     # To use sys.exit()


# Function to extract the username from user's first response
def get_username(text):
    pattern = "(?:[Mm]y name is|[iI] am|[iI]'m)* *([^\n]+)" # using regex to extract name
    test_res = re.match(pattern, text) #matching the pattern and user's input
    username = test_res.groups()[0]
    return username

# Chatbot responses - Dictionary
response_vocab = {
    r'[Ii] am (.*)':
        [
        "Why are you {}?",
        "Why do you feel {}?",
        "Can you tell me how long you've been {}?"
         ],

    r'[Ii] will (.*)':
    [
    "Why will you {}?",
    "Why do you feel that {}?"
    ],

    r'[Ii] want (.*)':
    [
        "Why do you want {}?",
        "What would it mean to you if you got {}?",
        "Will you feel better if you get {}?"
    ],

    r'[iI] don\'t want (.*)':
    [
        "Why don't you want {}?",
        "What makes you not want {}?"
    ],

    r'[iI] can\'t (.*)':
    [
        "What would be most helpful for you right now {}?",
        "What makes you think you can't {}?",
        "You might able to {} if you tried"
    ],

    r'[iI] feel (.*)':
    [   "Why do you feel {}?",
        "What makes you feel {}?",
        "Do you feel {} because of someone?",
        "Why are you feeling {}?"
    ],

    r'[Ii] love (.*)':
        [
            "Why do you love {}?",
            "Can you tell me little bit more about {}?"
        ],

     r'(.*)sad|depressed(.*)':
       [
        "Why are you sad?",
        "What can we do to make you happy?",
        "Don't worry, I hope things better"
        ],
    r'[want|need] your help':
    [
        "I am here to help you",
        "Please go on. I am here to help you",
        "I am always ready to help you"
    ],
    r'(.*)suicide|kill|die(.*)':
        [
            "Thank you for sharing with me.Things will be better soon",
            "Try to remember your happy moment. You will feel good",
            "How long have you had such thoughts for?",
            "Take a deep breath.Don't worry about anything"
        ],
    r'(.*)fear(.*)':
        [
            "Tell me more about your fear",
            "Is there something that is bothering you?",
        ],
    r'[iI] hate(.*)':
    [
         "Why do you hate {}?",
         "Tell me more about this"
    ],

    r'[tT]hank [yY]ou':
    [
        "You are welcome",
        "No Problem"
    ],
    r'(.*)okay|yes|no(.*)':
    [
      "Go ahead. Please tell me more.",
      "Tell me more about it"
    ],
    r'[hH]ow are you(.*)':
    [
        "I am fine, thank you.",
        "I'm doing good. how about you?",
        "I'm good. Hope you are doing good as well"
    ],
    r'(.*)happy(.*)':
    [
      "Good to know. Tell me the reason",
      "May you always stay like this"

    ],
# Default Response
    r'(.*)':
    [
        "I am unable to understand,can you tell me little bit more?",
        "I didn't quite understand that. Can you say it in another way ?"
    ]
}

#pronoun_vocab is used to convert first person pronoun to second person pronoun and vice-versa
pronoun_vocab = {
    "i":"you",
    "me":"you",
    "i will":"you will",
    "i am":"you are",
    "i have":"you have",
    "i would":"you would",
    "my":"your",
    "mine":"yours",
    "you": "me",
    "your":"my",
    "yours": "mine",
    "you have":"i have",
    "you would":"i would",
    "you are":"i am",
    "myself":"yourself"
}

# pronoun_convert function will convert from first to second person pronoun and vice-versa
def pronoun_convert(result):
    split_words = result.split(' ') #decompose a message into words
    for word in split_words:
        if word in pronoun_vocab.keys():
            index = split_words.index(word)    #take the index of the pronoun
            split_words[index] = pronoun_vocab[word]  #replacing detected pronoun with its appropriate form--> "my" will be "your"
    return ' '.join(split_words)                      #join the message with coverted pronoun

#This respond_to function will match input text with response_vocab dictionary and return corresponding responses
def respond_to(message):
    flag = 0
    if re.search(r'[Bb]ye|[Qq]uit', message):
        print("Eliza: " + "Bye, thank you for chatting")  # if input message is bye or quit, it will provide this message as output
        sys.exit()   # calling system exit to end the program

    for k, v in response_vocab.items():
        #print("Hello")
        res = re.search(k, message)   #search if input message matches the key of the response_vocab dictionary
        if res:
            response=random.choice(v)  # if matches, randomly chooses one response
            #print("Ok")
            if "{}" in response:       #check if the selected response includes "{}"
                res1=pronoun_convert(res[1])    #if any pronoun exists in res,it will convert it
                response=response.format(res1)   #merge the response and text after pronoun conversion
                print("Eliza: "+ response)
            else:
                print("Eliza: "+ response)      #If the response doesn't have {} then it choses a random response from the list of values
            flag=1
            break


# Initiating Chat here
username = get_username(input("Eliza: " + "Hi, I'm Eliza, your e-psychotherapist! What is your name? \n"))   #initial_text
# initial_text = input('Hi ' + username + ', How can I help you today ?\n')
print("Eliza: " +'Hi ' + username + ', How can I help you today ?')

# For the conversation to continue until a bye or exit is received
while 1:
    respond_to(input(username + ": "))