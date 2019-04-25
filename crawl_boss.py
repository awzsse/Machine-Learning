#!/usr/bin/env python
# coding: utf-8

# In[41]:


import requests
from bs4 import BeautifulSoup as bs

boss_headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}
r = requests.get('https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&city=101010100&industry=&position=',
                headers = boss_headers)
page = r.text
soup = bs(page, 'lxml')
soup.prettify()
base_boss_url = "https://www.zhipin.com"
job_index = []

all_jobs = soup.find_all("div", class_="job-primary")
for i in all_jobs:
    job_link = i.a["href"]
    job_title = i.a.find('div', class_= "job-title").text
    job_salary = i.a.span.text
    company_info = i.find("div", class_="info-company")
    company_url = company_info.a["href"]
    company_name = company_info.a.text
    company_status = company_info.p.text
    publish_info = i.find("div", class_="info-publis")
    publish_date = publish_info.p.text

    job_index.append([base_boss_url+job_link,job_title,job_salary,
                  base_boss_url+company_url,company_name,company_status,publish_date])
    
job_index

