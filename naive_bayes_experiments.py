#!/usr/bin/env python
# coding: utf-8

# # CSC421 Assignment 3 - Part II Naive Bayes Classification (5 points) #
# ### Author: George Tzanetakis 
# 
# This notebook is based on the supporting material for topics covered in **Chapter 13 Quantifying Uncertainty**and **Chapter 20 - Statistical Learning Method** from the book *Artificial Intelligence: A Modern Approach.* This part does NOT rely on the provided code so you can complete it just using basic Python. 
# 
# ```
# Misunderstanding of probability may be the greatest of all impediments
# to scientific literacy.
# 
# Gould, Stephen Jay
# ```
# 
# 

# # Introduction 
# 
# 
# Text categorization is the task of assigning a given document to one of a fixed set of categories, on the basis of text it contains. Naive Bayes models are often used for this task. In these models, the query variable is
# the document category, and the effect variables are the presence/absence
# of each word in the language; the assumption is that words occur independently in documents within a given category (condititional independence), with frequencies determined by document category. Download the following file: http://www.cs.cornell.edu/People/pabo/movie-review-data/review_polarity.tar.gz
# 
# 
# Our goal will be to build a simple Naive Bayes classifier for this dataset. More complicated approaches using term frequency and inverse document frequency weighting and many more words are possible but the basic concepts
# are the same. The goal is to understand the whole process so DO NOT use existing machine learning packages but rather build the classifier from scratch.

# Our feature vector representation for each text file will be simply a binary vector that shows which of the following words are present in the text file: Awful Bad Boring Dull Effective Enjoyable Great Hilarious. For example the text file cv996 11592.txt would be represented as (0, 0, 0, 0, 1, 0, 1, 0) because it contains Effective and Great but none of the other words.

# Write code that parses the text files and calculates the probabilities for
# each dictionary word given the review polarity

# In[79]:

import os
import numpy
import random

neg_files = os.listdir("txt_sentoken/neg")
pos_files = os.listdir("txt_sentoken/pos")

neg_dic, neg_probs = calcProb(neg_files, 'txt_sentoken/neg/')
pos_dic, pos_probs = calcProb(pos_files, 'txt_sentoken/pos/')

print(neg_probs)
print(pos_probs)


# In[80]:


def calcProb(files, link):
    
    dictionary_list=[]
    probs = []

    awful = 0;
    bad = 0;
    boring = 0;
    dull = 0;
    effective = 0;
    enjoyable = 0;
    great = 0;
    hilarious = 0;

    for file in files:
        dictionary = []
        file = link + file
        f = open(file, "r")
        review = f.read()
        if ('awful' or 'Awful') in review:
            dictionary.append(1)
            awful += 1
        else:
            dictionary.append(0)
        if ('bad' or 'Bad') in review:
            dictionary.append(1)
            bad += 1
        else:
            dictionary.append(0)
        if ('boring' or 'Boring') in review:
            dictionary.append(1)
            boring += 1
        else:
            dictionary.append(0)
        if ('dull' or 'Dull') in review:
            dictionary.append(1)
            dull += 1
        else:
            dictionary.append(0)
        if ('effective' or 'Effective') in review:
            dictionary.append(1)
            effective += 1
        else:
            dictionary.append(0)
        if ('enjoyable' or 'Enjoyable') in review:
            dictionary.append(1)
            enjoyable += 1
        else:
            dictionary.append(0)
        if ('great' or 'Great') in review:
            dictionary.append(1)
            great += 1
        else:
            dictionary.append(0)
        if ('hilarious' or 'Hilarious') in review:
            dictionary.append(1)
            hilarious += 1
        else:
            dictionary.append(0)
        f.close()
        dictionary_list.append(dictionary)
    
    #none were = 0 so I didn't bother with +1
    probs.append(awful/1000)
    probs.append(bad/1000)
    probs.append(boring/1000)
    probs.append(dull/1000)
    probs.append(effective/1000)
    probs.append(enjoyable/1000)
    probs.append(great/1000)
    probs.append(hilarious/1000)
    
    return dictionary_list, probs


# # Question 2B (Minimum) (CSC421 - 1 point, CSC581C - 0 point) 
# 
# 
# Explain how the probability estimates for each dictionary word given the review polarity can be combined to form a Naive Bayes classifier. You can look up Bernoulli Bayes model for this simple model where only presence/absence of a word is modeled.
# 
# Your answer should be a description of the process with equations and a specific example as markdown text NOT python code. You will write the code in the next questinon. 

# # Answer 2B
# 
# Our Data is like this:
# 
# awful | bad | boring | effective | enjoyable | great | hilarious
# 
# label
# 
# For example, cv996 11592.txt:
# 
# data = 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0
# label = pos
# 
# In Naive Bayes, each feature is considered to be independant of each other. Therefore, our Naive Bayes Classifier looks like this.
# 
# The probability of trait set X given label Y is the product of the following for all x_i in (x_1, ..., x_n):
# 
# (P(label = Y | x_i)^x_i)(P(label != Y | x_i)^(1-x_i))
# 
# Which, when there is only binary data, simplifies to this:
# 
# P(label = Y | x_i)
# 
# For this example, it would be as follows:
# 
# P(data | pos) = P(pos | x_1 = 0) x P(pos | x_2 = 0) x P(pos | x_3 = 0) x P(pos | x_4 = 0) x P(pos | x_5 = 1) x P(pos | x_6 = 0) x P(pos | x_7 = 1) x P(pos | x_8 = 0)
# 
# = (1-0.034) x (1-0.28) x (1-0.054) x (1-0.025) x 0.154 x (1-0.096) x 0.485 x (1-0.132)
# 
# P(data | neg) = P(neg | x_1 = 0) x P(neg | x_2 = 0) x P(neg | x_3 = 0) x P(neg | x_4 = 0) x P(neg | x_5 = 1) x P(neg | x_6 = 0) x P(neg | x_7 = 1) x P(neg | x_8 = 0)
# 
# = (1-0.122) x (1-0.545) x (1-0.175) x (1-0.101) x 0.086 x (1-0.054) x 0.32 x (1-0.059)
# 
# The higher value of the two is the predicted class. Ideally, it matches the correct label, positive. I'm pretty sure it's not normalised, so it's the actual probability.

# # Question 2C (Expected) 1 point 
# 
# Write Python code for classifying a particular test instance (in our case movie review) following a Bernolli Bayes approach. Your code should calculate the likelihood the review is positive given the correspondng conditional probabilities for each dictionary word as well as the likelihood the review is negative given the corresponding conditional probabilities for each dictionary word. Check that your code works by providing a few example cases of prediction. Your code should be written from "scratch" and only use numpy/scipy but not machine learning libraries like scikit-learn or tensorflow. 
# 

# In[81]:


# YOUR CODE GOES HERE 

test = [0, 0, 0, 0, 1, 0, 1, 0]; #play with this to vary tests

def classify(test, p, n):
    prod = 1;
    #calc positive chance
    for feature in range(len(test)):
        if(test[feature] == 0):
            prod = prod*(1-p[feature])
        if(test[feature] == 1):
            prod = prod*p[feature]

    pos = prod;

    prod = 1
    #calc negative chance
    for feature in range(len(test)):
        if (test[feature] == 0):
            prod = prod*(1-n[feature])
        if(test[feature] == 1):
            prod = prod*n[feature]

    neg = prod;

    res = 'positive'
    if (max(pos, neg) == neg):
        res = 'negative'

    return res
    
result = classify(test, pos_probs, neg_probs)
print("This is probaby a %s review." %result)


# # QUESTION 2D (Expected ) 1 point

# Calculate the classification accuracy and confusion matrix that you would obtain using the whole data set for both training and testing. Do not use machine learning libraries like scikit-learn or tensorflow for this only the basic numpy/scipy stuff. 

# In[82]:


# YOUR CODE GOES HERE
#Note for myself:
#What we're getting here is the training error, not the testing
#error, since it's being tested on the training set, I think.

dictionary = pos_dic + neg_dic
results = [];

for review in dictionary:
    results.append(classify(review, pos_probs, neg_probs))

accuracy = 0;
tp = 0;
tn = 0;
fp = 0;
fn = 0;

for x in range(1000):
    if(results[x] == 'positive'):
        accuracy = accuracy + 1
        tp = tp + 1
    else:
        fp = fp + 1
    if(results[999+x] == 'negative'):
        accuracy = accuracy + 1
        tn = tn + 1
    else:
        fn = fn + 1
        
accuracy = accuracy/2000
confusion_matrix = [[tp, fn], [fp, tn]]

print(accuracy) #0.6705. It's better than guessing randomly!
print(confusion_matrix) #1341 out of 2000 were correct.


# # QUESTION 2E (Advanced) 1 point 
# 
# One can consider the Naive Bayes classifier a generative model that can generate binary feature vectors using the associated probabilities from the training data. The idea is similar to how we do direct sampling in
# Bayesian Networks and depends on generating random number from a discrete distribution. Describe how you would generate random movie reviews consisting solely of the words from the dictionary using your model. Show 5 examples of randomly generated positive reviews and 5 examples of randomly generated negative reviews. Each example should consists of a subset of the words in the dictionary. Hint: use probabilities to generate both the presence and absence of a word

# # Answer 2E
# 
# The approach here is to grab eight random numbers corrosponding to the probabilities that each word is used in a given review.

# In[83]:


# YOUR CODE GOES HERE 

positive_reviews = [];
negative_reviews = [];

dictionary = ['awful', 'bad', 'boring', 'dull', 'effective', 'enjoyable', 'great', 'hilarious'];

neg_probs
pos_probs

temp = 0;
print('Some negative reviews:')
for y in range(5):
    review = []
    for x in range(8):
        temp = random.randrange(0, 1000)
        if temp < (1000*neg_probs[x]):
            review.append(dictionary[x])
    print(review);

temp = 0;
print('Some positive reviews:')
for y in range(5):
    review = []
    for x in range(8):
        temp = random.randrange(0, 1000)
        if temp < (1000*pos_probs[x]):
            review.append(dictionary[x])
    print(review);


# # QUESTION 2F (ADVANCED) (CSC421 - 0 points, CSC581C - 2 points)
# 
# Check the associated README file and see what convention is used for the 10-fold cross-validation. Calculate the classification accuracy and confusion matrix using the recommended 10-fold cross-validation. Again do NOT use 
# ML libraries such as scikit-learn or tensorflow and just use numpy/scipy. 

# In[50]:


# YOUR CODE GOES HERE 

