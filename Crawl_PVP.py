#!/usr/bin/env python
# coding: utf-8

# In[139]:


import requests
import json
from bs4 import BeautifulSoup as bs


# In[141]:


r = requests.get("https://pvp.qq.com/web201605/js/herolist.json", stream = True) #先把网络信息存到r中

with open("allhero.json", "wb") as fd: #创建一个文件，把r信息存入，关闭文件
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)


# In[143]:


hero_list = None #准备将文件信息再次读取，但是这里是json的数据格式，读取出来类似字典，但是其key必须是字符串,如果不恢复，无法使用hero_list
with open("allhero.json", "rb") as json_data:
    hero_list = json.load(json_data) #json.load是对文件操作，json.loads是对字符串操作。对应dump以及dumps
    print(hero_list)


# In[144]:


def search_for_hero_info(name=None):
    for hero in hero_list:
        if "cname" in hero:
            if hero["cname"] == name:
                return hero
    return None


# In[145]:


hero_list[12]


# In[146]:


hero_type = ["全部","战士","法师","坦克","刺客","射手","辅助"] #根据网页上信息归纳总结，发现0到6对应的是这几个


# In[147]:


def build_hero_type(hero):
# for hero in hero_list: #遍历json数据结构，对每个英雄对象中type信息进行赋值，重新加入一个新的list
    combined_type = []
    if "hero_type" in hero:
        combined_type.append(hero_type[hero["hero_type"]])
    if "hero_type2" in hero:
        combined_type.append(hero_type[hero["hero_type2"]])
    if "new_type" in hero:
        combined_type.append(hero_type[hero["new_type"]])
    return ("|".join(combined_type))


# In[148]:


from selenium import webdriver #如果有些网页用的javascript写的，有时候提取信息看不出来，这时就需要使用webdriver去重新渲染

browser = webdriver.Chrome('./chromedriver')
browser.get("https://pvp.qq.com/web201605/herolist.shtml")
html = browser.page_source
browser.quit()


# In[149]:


with open("hero_web.html", 'w',encoding="utf-8") as fd:
     fd.write(html)


# In[150]:


hero_html = None
with open("hero_web.html", 'r',encoding="utf-8") as fd:
     hero_html = fd.read()
hero_html


# In[151]:


heropage_soup = bs(hero_html, "lxml") #先把hero_html变成一个bs对象，后续才能开始利用bs功能寻找字段筛选
hero_html_list = heropage_soup.find("ul", class_="herolist") #该页面上所有关于英雄的信息的集合，除去别的标题，如活动之类
all_hero_list = hero_html_list.find_all("li")#将每个英雄加入list中
gen_hero = [[i.text, i.img["src"].strip("/")] for i in all_hero_list] #其中i.text是在li下的英雄信息部分，i.img是在英雄信息下的图片信息，而由于前面有//要去掉’/‘才能打开图片
gen_hero


# In[188]:


#设置一个可以装所有英雄，所有信息的list，具体信息包括[name，type，skin，url for pic]
def merge_hero_info(hero_info, hero_json): #这里的hero_info在本例中对应gen_hero，而hero_json对应hero_list
    combined_heros = []
    for hero in hero_info:
        hero_detail = search_for_hero_info(hero[0])
        combined_heros.append([hero[0], build_hero_type(hero_detail), hero_detail["skin_name"], hero[1]])
    return combined_heros


# In[189]:


combined_heros = merge_hero_info(gen_hero, hero_list)
# 当时程序运行到这里出现了个问题，就是有个英雄没有skin_name，因此我人为加入了一个，但是要记住重新写读文件以后又变回去了
combined_heros


# In[196]:


def get_keywords_array(hero):
    """
    根据英雄信息，生成keyword的列表
    [hero_name, hero_type, hero_skin, hero_url]
    """
    keywords =[]
    if hero[0]:
        keywords.append(hero[0])
    if hero[1]:
        keywords += hero[1].split('|')
    if hero[2]:
        keywords +=hero[2].split('|')
    return keywords

def add_to_index(index, keyword, info):
    """
    添加索引到搜索数据列表中
    """    
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(info)
            return
    #not find
    index.append([keyword,[info]])
    
def build_up_index(index_array):
    """
    创建搜索数据列表
    """        
    for hero_info in combined_heros:
        keywords = get_keywords_array(hero_info)
        for key in keywords:
            add_to_index(index_array,key,hero_info) 

# lookup information by keywords
def lookup(index,keyword):
    """
    根据关键词在列表中搜索
    """        
    for entry in index:
        if entry[0] == keyword:
            return entry[1] 
    #not find
    return entry[0] 

search_index=[]
build_up_index(search_index)

lookup(search_index,"关羽")

