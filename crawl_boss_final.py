#!/usr/bin/env python
# coding: utf-8

# In[54]:


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

all_jobs[100]


# In[56]:


all_jobs[11]


# In[113]:


job_desc = [] #开始爬具体每个职位里面的信息
for job in all_jobs[200:]:#在270个开始爬，不然太多了
    print(".",end="")
    job_detail = requests.request("GET", 'https://www.zhipin.com/job_detail/bdea84c54dc23c2c1HZ73NW-FlY~.html', headers = boss_headers)
    job_soup = bs(job_detail.text, "lxml")
    detail_text = job_soup.find("div", class_="job-sec").text.replace("\n","").replace(" ", "")
    job_desc = job_desc + [[job[0], detail_text]]
job_desc


# In[86]:


job_desc[1]


# In[76]:


import jieba #分词器，用来切分中文，用来制作词云
fenci = jieba.cut("我在武汉上大学，上的是比清华好的地质大学", cut_all = True)
print("/".join(fenci))


# In[118]:


combined_job_desc = " ".join([j[1].replace("\n","").replace(" ","") for j in job_desc]) #使用comprehension取出每个detail组成一大段文字


# In[123]:


fenci_job_desc = jieba.cut(combined_job_desc, cut_all = False)
space = " ".join(fenci_job_desc)
space


# In[120]:


from wordcloud import WordCloud, ImageColorGenerator #导入wordcloud
import numpy as np
from PIL import Image


# In[128]:


wc = WordCloud(
    background_color="white", #设置颜色
    max_words=200, #词的最大数量，默认值为200
    colormap='viridis',
    random_state=10, #多少种配色方案
    font_path='/Users/awzsse/Desktop/msyh.ttf', #自己下载了msyh.ttf放在桌面路径下
    stopwords=('能够','数据','业务','职位描述','数据分析','职责','工作职责','任职要求','描述','产品经验','产品','经验','熟练','进行','运营','以上学历','使用','工具','本科','提供','负责','业务','熟悉','优先','能力','策略')
)

my_wordcloud = wc.generate(space)


# In[ ]:





# In[129]:


import matplotlib.pyplot as plt #开始绘图
#可以直接在python consolo里面产生图像，如果在pycharm或者其他IDLE中会报错
get_ipython().run_line_magic('matplotlib', 'inline')

plt.imshow(my_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.figure()


# In[130]:


import jieba.analyse #感觉以上分类还是不够明晰，很多关键词没有提取出来，这里利用jieba的关键词分析工具
keywords = jieba.analyse.extract_tags(combined_job_desc, topK=300, withWeight=True, allowPOS=('n'))
keywords #例子，topK代表最多词汇量，withWeight代表带权重，allowPOS代表词性


# In[133]:


import re #删除所有中文的的例子
s = "hi新手oh"
remove_chinese = re.compile(r'[\u4e00-\u9fa5]') #[\u4e00-\u9fa5]是匹配所有中文的正则
print(remove_chinese.split(s))


# In[135]:


all_english = ''.join(remove_chinese.split(combined_job_desc))
all_english


# In[137]:


keywords = jieba.analyse.extract_tags(all_english, topK=300, withWeight=True, allowPOS=())
keywords


# In[138]:


eng_job_desc = jieba.cut(all_english, cut_all = False)
eng_space = " ".join(eng_job_desc)
eng_space


# In[139]:


wc = WordCloud(
    background_color="white", #设置颜色
    max_words=200, #词的最大数量，默认值为200
    colormap='viridis',
    random_state=10, #多少种配色方案
    font_path='/Users/awzsse/Desktop/msyh.ttf', #自己下载了msyh.ttf放在桌面路径下
    stopwords=('能够','数据','业务','职位描述','数据分析','职责','工作职责','任职要求','描述','产品经验','产品','经验','熟练','进行','运营','以上学历','使用','工具','本科','提供','负责','业务','熟悉','优先','能力','策略')
)

my_wordcloud = wc.generate(eng_space)

plt.imshow(my_wordcloud, interpolation="bilinear")
plt.axis("off")
plt.figure()

