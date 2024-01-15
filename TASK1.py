#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install requests')
get_ipython().system('pip install beautifulsoup4')


# In[3]:


import os
import requests
import re
from bs4 import BeautifulSoup


# In[5]:


# Function to get the html source text of the medium article
def get_page(url):
    # handling possible error
    if not url.startswith('https://medium.com/'):
        print('Please enter a valid Medium article URL.')
        sys.exit(1)

    # Call get method in requests object, pass url and collect it in res
    res = requests.get(url)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


# In[6]:


# Function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text


# In[7]:


# Function to collect text from the article
def collect_text(soup):
    text = ''
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text


# In[1]:


# Function to save file in the current directory
def save_file(text, url):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'

    with open(fname, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f'File saved in directory {fname}')


# In[ ]:


if __name__ == '__main__':
    url = input("Enter the URL of a Medium article: ")
    soup = get_page(url)
    text = collect_text(soup)
    save_file(text, url)

