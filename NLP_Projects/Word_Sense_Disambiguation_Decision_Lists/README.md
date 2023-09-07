Word Sense Disambiguation with Decision Lists

Goals of the project:
- To write a Python program called decision-list.py that implements a decision list classifier to perform word sense disambiguation. 
- Program uses features from the original Yarowsky's method 
-  Classifier should run from the command line as follows 
	- python decision-list.py line-train.xml line-test.xml my-decision-list.txt > my-line-answers.txt
- This command should learn a decision list from line-train.xml and apply that decision list to each of the sentences found in line-test.xml in order to assign a sense to the word line.
- Program outputs the decision list it learns to my-decision-list.txt
- line-train.xml contains examples of the word line used in the sense of a phone line and a product line where the correct sense is marked in the text (to serve as an example from which to learn). linetest.xml contains sentences that use the word line without any sense being indicated, where the correct answer is found in the file line-answers.txt
- scorer.py will take as input the sense tagged output and compare it with the gold standard "key" data in line-answers.txt. The scorer program will report the overall accuracy of the tagging, and provide a confusion matrix. The scorer program should be run as follows:
	- $ python scorer.py my-line-answers.txt line-answers.txt	



  



