#!/usr/bin/env python
# coding: utf-8

# ## AIT526 - Individual Lab 3

# In[1]:


from bs4 import BeautifulSoup
import requests


# In[2]:


import spacy
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from spacy import displacy


# In[3]:


# 1.1 - Web Scraping Technique
def get_content_from_page(url):
    
    final_page_text = ""
    
    page_response = requests.get(url)
    soup_response = BeautifulSoup(page_response.content, "lxml")
    final_content = soup_response.find(id="content")
    pars = final_content.find_all("p")
    
    for p in pars:
        final_page_text += p.text
        
    return final_page_text.lower()

URL = 'https://en.wikipedia.org/wiki/Russian_invasion_of_Ukraine'
content = get_content_from_page(URL)
content


# In[4]:


nlp = spacy.load('en_core_web_sm')

article_txt = nlp(content)

# 1.2.1 - Count all the named entities in the document  
print(len(article_txt.ents))

# The various entities present in the article are :
entity_labels = [x.label_ for x in article_txt.ents]
Counter(entity_labels)


# In[5]:


# 1.2.2 - Count the most frequent tokens for the entire document  

regular_exp = re.compile('^-?\\d*(\\.\\d+)?$')

article_tokens = []

for c in article_txt:
    #print(c.text)
    if regular_exp.match(c.text) is None: # should not match the given regular expression
        if not(nlp.vocab[c.text].is_stop): # should not be a stop word
            if not(nlp.vocab[c.text].is_punct): # should not be punctuation
                article_tokens.append(c.text)
                
Counter(article_tokens).most_common(10)


# In[6]:


# 1.2.3
# Printing K+3 sentences

import random  # to pick a random number

no_of_sentences = [s for s in article_txt.sents]
len(no_of_sentences)

max_sen_num = len(no_of_sentences) - 3 #cannot use last 2 numbers to print 3 sentences
chosen_sentences = []

K = random.randrange(max_sen_num)
print('The chosen random number is: ', K, '\n\n')
print('The sentences are: ', '\n')
for num in range(K, K+3):
    print('Sentence number', num, 'is: \n', no_of_sentences[num],'\n')
    chosen_sentences.append (no_of_sentences[num])


# In[7]:


# 1.2.4 - POS and Lemmatization of the above chosen sentences
for each_sent in chosen_sentences:
    for each_token in each_sent:
        if each_token.pos_ != 'PUNCT' and not each_token.is_stop:
            print(each_token.orth_, each_token.pos_, each_token.lemma_)


# In[8]:


# 1.2.5 - Entity Notation 
for each_sent in chosen_sentences:
    for entity_notation in each_sent.ents:
        print(entity_notation.text, '-->', entity_notation.label_)


# In[9]:


# 1.2.6 - Visualizing the entities and dependencies of the Kth sentence
displacy.render(chosen_sentences[2], style="ent")


# In[10]:


# Dependencies
displacy.render(chosen_sentences[2], style="dep")


# In[11]:


# 1.2.7 - Visualizing all the entities in the document
displacy.render(article_txt, style='ent')


# In[12]:


# 2.1 Part I - Deidentification

# Deidentifying the PERSON label
def deidentify_person(content):
    deidentification_res = []
    for x in nlp(content):
        if x.ent_type_ == 'PERSON':
            deidentification_res.append("[REDACTED]")
        else:
            deidentification_res.append(x.text)
    
    final_res = " ".join(deidentification_res)
    return final_res   


# In[13]:


res_without_person = deidentify_person(content)
print(res_without_person)


# In[14]:


# 2.1 part II - Visualizing the result from 2.1


displacy.render(nlp(res_without_person), style='ent')


# In[ ]:




