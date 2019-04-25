#!/usr/bin/env python
# coding: utf-8

# In[52]:


import requests
from bs4 import BeautifulSoup as bs

def extrac_jobs(page):
    page_soup = bs(page, 'lxml')
    page_soup.prettify()
    base_boss_url = "https://www.zhipin.com"
    job_index = []
    all_jobs = page_soup.find_all("div", class_="job-primary")

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

    el_page = page_soup.find("div", class_="page")
    next_url = el_page.find(attrs={"ka":"page-next"})["href"]
    return job_index, next_url

boss_headers = {
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

next_to_fetch = "https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&city=101010100&industry=&position="
counter = 0
all_jobs = []
while next_to_fetch != base_boss_url+"javascript:;":
    print("start to fetch url:"+ next_to_fetch)
    r = requests.request("GET", next_to_fetch, headers = boss_headers)
    page = r.text
    job_index, next_url = extrac_jobs(page)
    next_to_fetch = base_boss_url + next_url
    counter+=1
    
    if len(job_index) > 0:
        all_jobs = all_jobs + job_index
    if counter > 10:
        break

all_jobs

    

