Implement a Question Answering (QA) system in Python called qa-system.py

Goals of the QA system:
- The system should take an approach similar to that of the AskMSR system, and simply reformulate the question as a series of "answer patterns" that you then search for in Wikipedia, where you are hoping to find an exact match to one of your patterns. 

- The program should run interactively, and prompt the user for questions until the user says "exit".

- Then, a user should enter their question and the system should respond with an answer that is a complete sentence, and should not contain any information beyond that which is asked by the question. Note that this is not a conversational agent, so the system does not need to remember previous questions or answers, nor does it need to engage in "small talk". We may assume that the user will cooperate and only ask well-formed questions.

- You may assume that the questions are well formed and grammatical, and that they are in fact questions. You may assume that all questions start with either Who, What, When or Where. The system should recognize when it can't answer a question, and say something like "I am sorry I don't know the answer." This is preferable to giving no answer or providing gibberish. 

        $ python qa-system.py mylogfile.txt
        *** This is a QA system by YourName. It will try to answer questions that start with Who, What, When or Where. Enter "exit" to leave the program.
        =?> When was George Washington born? (user)
        => George Washington was born on February 22, 1732. (system)
        =?> What is a bicycle?
        => A bicycle has two wheels and is used for transportation.
        =?> Where is Duluth, Minnesota?
        =>I am sorry, I don't know the answer.
        =?> exit    
        Thank you! Goodbye.


