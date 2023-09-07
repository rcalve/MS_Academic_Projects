Eliza Chatbot

Objective : The main objective of this assignment is to build a chatbot that plays the role of a psychotherapist,
             similar to the working of Eliza.
             This code will showcase the implementation of using regular expressions, word spotting, sentence
             formation and various other functions that help in capturing text and generating appropriate responses.

How does our chatbot work ?
   1. The chatbot initially asks for the user's name and extracts it from the response.
   2. All the following responses will have the user's name to the left to know whose response it is.
   3. Post the extraction of the name, based on the user's input, our program searches through the predefined
      dictionary that has a set of regular expressions as the keys and some predefined responses as a list
      in the values.
      If a match is found, then it picks a random response from the set of predefined values.
   4. It is then passed through a dictionary to change the pronouns. Eg) me is changed to you
   5. One of the goals of this assignment is to extract parts of the question and use it in the response. We have
      accomplished this using {} in the predefined responses. Places where {} are found are the places where parts
      extracted from the users response are used in Eliza's response.
       For example, the user says - i am sad
       Eliza's response would be - Why are you sad ?
   6. When Eliza is unable to recognize the user's question/response, a default answer will be returned.
   7. Words like bye, Bye, quit and Quit are used to end the conversation with the user.

Points to remember while using our Chatbot
    1.  The chatbot that we have built is currently running with only minimal set of responses. We have around 18
        responses that our chatbot is currently able to recognize and respond back.
    2.  For responses that the chatbot is unable to recognize or does not have a predefined response in the dictionary,
        it returns a set of default responses -
        --  "I am unable to understand,can you tell me little bit more?",
        --  "I didn't quite understand that. Can you say it in another way ?"
    3.  When asked for your name, please respond back in one of the following ways :
          a) My name is ABC
          b) I am ABC
          c) I'm ABC
          d) ABC