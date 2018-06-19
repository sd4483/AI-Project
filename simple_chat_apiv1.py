
# coding: utf-8

# In[1]:
from flask import Flask, redirect, url_for, request, render_template, jsonify
from bs4 import BeautifulSoup as bs
import requests

import nltk
from nltk.tokenize import word_tokenize
import random
import numpy as np
from textblob import TextBlob

app = Flask(__name__)

# In[2]:



counter = 0
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
match =[]

GREETING_KEYWORDS = ("hello", "hi", "greetings", "hey", "whazzup")

GREETING_RESPONSES = ["hi hi", "hey", "*nods*", "good day", "oh, its you", "you talking to me ?"]


SYMPTOM1_KEYWORDS = ("fever", "headache", "joint", "pain", "muscle", "pain", "skin", "rashes", "Nausea", "Vomiting","Bleeding", "of", "Nose","gum", "bleeding")
SYMPTOM2_KEYWORDS = ("chills", "headache", "nausea", "vomiting", "diarrhea", "muscle", "pain", "convulsions", "bloody", "stools", "anemia", "fever", "abdominal", "pain")
SYMPTOM3_KEYWORDS = ("fever", "rash", "joint", "pain", "conjuctivitis", "muscle", "pain", "eye", "pain", "vomiting", "red", "eyes")
SYMPTOM4_KEYWORDS = ("sore", "throat", "runny", "nose", "cough", "fever", "body", "ache", "poor", "appetite", "abdominal", "pain", "diarrhea", "body", "ache", "vomiting")
SYMPTOM5_KEYWORDS = ("poor", "appetite", "headache", "body", "ache", "abdominal", "pain", "lethargy", "diarrhea")
SYMPTOMS_RESPONSES = ["You are likely to suffer from Dengue virus", "you are likely to suffer from malaria", "you are likely to suffer from zika", "you are likely to suffer from viral fever", "you are likely to suffer from typhoid"]


# In[3]:


def greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    sentence = word_tokenize(sentence)
    for word in sentence:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
        else:
            return None


# In[4]:


def preprocess(text):
    text = text.correct()
    # text = text.lower()
    clean_text = ' '.join(text.words)
    clean_text = clean_text.replace('charcot', 'chatbot')
    return clean_text


# In[5]:


def find_noun(text_tags):
    noun = None
    for word, pos in text_tags:
        if pos == 'NN':  # NN is short for noun
            noun = word
            break
    return noun    


# In[6]:


def find_verb(text_tags):
    verb = None
    partofspeech = None
    for word, pos in text_tags:
        if pos.startswith('VB'):  # any form of verb
            verb = word
            partofspeech = pos
            break

    return verb, partofspeech


# In[7]:


def find_adjective(text_tags):
    adjective = None
    for word, pos in text_tags:
        if pos == 'JJ':  # This is an adjective
            adjective = word
            break

    return adjective


# In[8]:


def find_response_pronoun(text_tags):
    response_pronoun = None
    for word, pos in text_tags:
        # Disambiguate pronouns
        if pos == 'PRP' and (word == 'you' or word == 'You'):
            response_pronoun = 'I'
        elif pos == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            response_pronoun = 'You'
        elif pos == 'PRP':
            response_pronoun = word

    return response_pronoun


# In[9]:


SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "Turn left and then right for the {noun} , the pharmacy is right there. ",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "What is the purpose of {noun}",
    "What can I do for {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I can help you with {adjective} ",
    "I can book a appointment for {adjective}",
]


# In[10]:


def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


# In[11]:


def symptoms(keywords, counter, counter1, counter2, counter3, counter4,match):
    
    for elements in keywords:
        if elements.lstrip() in SYMPTOM1_KEYWORDS:
            counter +=1
    match.append(counter)

    for elements in keywords:
        if elements.lstrip() in SYMPTOM2_KEYWORDS:
            counter1 +=1
    match.append(counter1)

    for elements in keywords:
        if elements.lstrip() in SYMPTOM3_KEYWORDS:
            counter2 +=1
    match.append(counter2)

    for elements in keywords:
        if elements.lstrip() in SYMPTOM4_KEYWORDS:
            counter3 +=1
    match.append(counter3)

    for elements in keywords:
        if elements.lstrip() in SYMPTOM5_KEYWORDS:
            counter4 +=1
    match.append(counter4)

    while(len(set(keywords)&set(SYMPTOM1_KEYWORDS)) is 0 and
            len(set(keywords)&set(SYMPTOM2_KEYWORDS)) is  0 and
            len(set(keywords)&set(SYMPTOM3_KEYWORDS)) is 0 and
            len(set(keywords)&set(SYMPTOM4_KEYWORDS)) is 0 and
            len(set(keywords)&set(SYMPTOM5_KEYWORDS)) is 0 ):
                return "Tell a valid symptom"
                

    values = np.array(match)
    searchval = max(match)
    i = np.where(values == searchval)[0]

    if (len(i)>1):
        return "do you have anymore symptoms?"
         
        """
        question = input('bot : Do you have anymore symptoms?')
        if (question =='yes'):
            question = input("bot : what are the other symptoms?")
            question = question.replace(',', ' ')
            localKey = question.split(' ')
            while(len(set(localKey)&set(SYMPTOM1_KEYWORDS)) is 0 and
            len(set(localKey)&set(SYMPTOM2_KEYWORDS)) is  0 and
            len(set(localKey)&set(SYMPTOM3_KEYWORDS)) is 0 and
            len(set(localKey)&set(SYMPTOM4_KEYWORDS)) is 0 and
            len(set(localKey)&set(SYMPTOM5_KEYWORDS)) is 0 ):
                question = input("bot : Tell a valid symptom !!")
                question = question.replace(',', ' ')
                localKey = question.split(' ')

            keywords += question.split(' ')
            i=[]
            symptoms(keywords, counter, counter1, counter2, counter3, counter4, match =[])
        elif(question == 'no'):
                print('bot : Please go for general check up')
        """
    else:
        for elements in i:
            return SYMPTOMS_RESPONSES[elements]



# In[12]:


NONE_RESPONSES = [
    "I have no idea what you've just said",
    "huh ? can you repeat that",
    "please say that again",
    "can you rephrase that ?",
    "I don't understand",
    "Whats the pupose of your visit to the hospital?",
]

COMMENTS_ABOUT_SELF = [
    "You may be right",
    "Do you really think so ?",
    "How can I help you?",
    "We find ways to do it",
    "I take that as a compliment"
]


# In[13]:


def respond(ques):
    
    resp = greeting(ques)
    
    # return greeting response if ques is greeting
    if resp:
        return resp
    
    # if not greeting, then determine a suitable response
    if not resp:
        # preprocess question
        text = TextBlob(ques)
        clean_text = preprocess(text)
        
        # find parts of speech
        text = TextBlob(clean_text)
        text_tags = text.tags
        
        noun = find_noun(text_tags)
        verb = find_verb(text_tags)
        adjective = find_adjective(text_tags)
        response_pronoun = find_response_pronoun(text_tags)
        
        # comments about bot
        if response_pronoun == 'I' and (noun or adjective):
            if noun:
                if random.choice((True, False)):
                    resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
                    return resp
                else:
                    resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
                    return resp
            else:
                resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective}) 
                return resp
        
        # comments about self
        if response_pronoun == 'I' and verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
            return resp

        # construct own response
        resp = []

        if response_pronoun:
            resp.append(response_pronoun)

            if verb:
                verb_word = verb[0]
                if verb_word in ('be', 'am', 'is', "'m"):  
                    if response_pronoun.lower() == 'you':
                        resp=("What are the symptoms of your sickness?")
                        return "".join(resp)
                    else:
                        resp.append(verb_word)
                        return " ".join(resp)
                    
                    

            if noun:
                if response_pronoun.lower() == "i":
                    prop_noun = "am"
                elif response_pronoun.lower() == "you":
                    prop_noun = "are" 
                elif response_pronoun.lower == ("he" or "she" or "it"):
                    prop_noun = "is" 
                elif response_pronoun.lower == ("they" or "we"):
                    prop_noun = "are"
                else:
                    prop_noun = "is"
                a_or_an = "an" if starts_with_vowel(noun) else "a"
                resp.append(prop_noun + " " + a_or_an + " " + noun)

                # choose a none response if it does not meet any of the crtieria above
            else:
                resp = random.choice(NONE_RESPONSES)
                return resp          

            resp.append(random.choice(("la", "bro", "lol", "bruh", "")))

            resp = " ".join(resp)
        
    
        
        else:
            resp = "I am still under development, so i dont understand that"
        
    return resp   


# In[ ]:

@app.route('/hi')
def loadPage():

    #return jsonify(items=[dict(a="one", b="two"), dict(c=3, d=4)], forecasts=[dict(a=1, b=2), dict(c=3, d=4)])

    return jsonify(items=[dict(a="one", message ='Good day, I am a reception assistant. How may I help you today?')])

@app.route('/sick', methods=['GET'])
def sick():
    return jsonify(items=[dict(a="one", message ='What are the symptoms of your sickness?')])


@app.route('/symptoms/<string:name>', methods=['GET'])
def symptom(name):
    question = name
    question = question.replace('_', ' ')
    keywords = question.split(' ')
    a = symptoms(keywords, counter, counter1, counter2, counter3, counter4, match =[])
    return jsonify(items=[dict(a="one", message =a)],match = match)




@app.route('/more_symp/<string:name>', methods=['GET'])
def more_symp(name):
    if (name.lower() == 'yes'):
        return jsonify(items=[dict(a="one", message ="What are the other symptoms?")])
    elif (name.lower() == 'no'):
        return jsonify(items=[dict(a="one", message ="Please go for general check up")])

    
@app.route('/other_symp/<string:name>', methods=['GET'])
def other_symp(name):
    if (name.lower() == 'yes'):
        return jsonify(items=[dict(a="one", message ="What are the other symptoms?")])
    elif (name.lower() == 'no'):
        return jsonify(items=[dict(a="one", message ="Please go for general check up")])



            #symptoms(keywords, counter, counter1, counter2, counter3, counter4, match = [])

    """
    question = input('Good day, I am a recption assistant. How may I help you today?  ')

    while question != "bye bye":
        if ('emergency' in question):
            print('Calling emergency doctor..')
            break
        elif ('sick' in question or 'doctor' in question or 'not feeling well' in question or 'MC' in question):
            question = input('What are the symptoms of your sickness?')
            question = question.replace(',', ' ')
            keywords = question.split(' ')
            counter = 0
            counter1 = 0
            counter2 = 0
            counter3 = 0
            counter4 = 0
            match =[]
            symptoms(keywords, counter, counter1, counter2, counter3, counter4, match = [])
            break
                
        else:
            answer = respond(question)
            print ('bot : ', answer)
            print ('')  
            question = input('say something : ')
    
    """
if __name__ == '__main__':
    app.run(debug=True)

#print ("Hope I served you well")


