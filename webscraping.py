#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import BeautifulSoup for pulling data out of HTML and XML files
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests
import random


# In[2]:


#import selenium for web scraping
from selenium import webdriver
from bs4 import BeautifulSoup
from requests import get
import pandas as pd


# In[ ]:


#import chromedriver
driver = webdriver.Chrome("chromedriver")

#open google scholar via url
driver.get('https://scholar.google.com/citations?view_op=view_org&hl=en&org=10241031385301082500')


# In[3]:


author = pd.DataFrame(columns=['user_ID','name','affiliation'])


# In[4]:


row = 0
while True:
    
    
    all_ele = driver.find_elements_by_class_name('gsc_1usr')
    for i in all_ele:
        link = i.find_element_by_class_name('gs_ai_pho')
        id = str(link.get_attribute('href')).replace('https://scholar.google.com/citations?hl=en&user=','')
        name = i.find_element_by_class_name('gs_ai_name')
        name = name.text 
        af = i.find_element_by_class_name('gs_ai_aff')
        af = af.text
        author.loc[row]=[id,name,af]
        row +=1
   
    
    page = requests.get(driver.current_url)
    soup = BeautifulSoup(page.content)
    results = soup.find_all(class_='gs_btnPR')
    if results[0].has_attr('onclick'):
        driver.find_element_by_css_selector(".gs_btnPR").click()
    else:
        break
    time.sleep(random.randint(2,5))


# In[5]:


driver.close()


# In[6]:


author


# In[7]:


paper = pd.DataFrame(columns=['title','authors','publication_date','description','cite_by'])


# In[8]:


driver = webdriver.Chrome("chromedriver")
row = 0
re = 0
for usr_id in author['user_ID']:
    driver.get('https://scholar.google.com/citations?hl=en&user='+usr_id)

    a=driver.find_elements_by_class_name('gs_btnPD')
    while a[0].is_enabled()==True:
        driver.find_element_by_class_name('gs_btnPD').click()
        time.sleep(3)
    link = driver.find_elements_by_class_name('gsc_a_at')
    link = [i.get_attribute('data-href') for i in link]
    print(len(link))

    for url in link:
        driver.get('https://scholar.google.com/'+url)
        try :
            
            table = driver.find_element_by_id('gsc_vcd_table')
            b = table.find_elements_by_class_name('gs_scl')
            title =''
            Au = ''
            PD = ''
            Des = ''
            cited = ''
            for i in b:
                title = driver.find_elements_by_class_name('gsc_vcd_title_link')[0].text
                if i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Authors':
                    Au = i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Publication date':
                    PD =i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Description':
                    Des =i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Total citations':
                    cited =i.find_elements_by_css_selector('a')[0].text.replace('Cited by ','')

            paper.loc[row]=[title,Au,PD,Des,cited]
            row += 1
        except :
            pass
        
        print('people pass',re)
        print('no.',len(paper))
        time.sleep(2)
    re += 1


# In[9]:


paper


# In[10]:


driver.close()  


# In[11]:


author.to_csv('author.csv')
paper.to_csv('paper.csv')





