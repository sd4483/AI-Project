# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:37:00 2018

@author: sudhe
"""

from bs4 import BeautifulSoup as bs
import requests

question = input("Ask me anything : ")

question = question.split()
question = "_".join(question)

url = 'http://www.answers.com/Q/' + question

content = response.text
response = response.get(url)

soup = bs(content, 'html.parser')

ans = soup.find('div', {'class' : 'answer_text'}); ans

ans = ans.replace('\n', " ")

def response(question):
    
    question = "_".join(question.split())
    url = 'http://www.answers.com/Q/' + question
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    ans = soup.find('div', {'class' : 'answer_text'}).text.strip().replace('\n', " ")
    
    return ans

question = input("Ask me anything : ")

while question != "bye":
    reply = response(question)
    print (reply,'\n')
    question = input("Ask me anything : ")
    
print ('goodbye')

