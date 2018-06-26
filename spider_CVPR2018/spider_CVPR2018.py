# -*- coding :utf-8 -*-
import os

import re
import threading
import urllib2
from bs4 import BeautifulSoup
from multiprocessing import Queue
import io
import requests
import pdfkit
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'xt'

url_paperhome = "http://openaccess.thecvf.com/CVPR2018.py"
download_home = "http://openaccess.thecvf.com/"
dir_save = "save2\\"

header =  {'User-Agent':'Mozilla/5.0(Windows NT 6.1)AppleWebKit/537.11(KHTML,like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept':'text/html; q=0.9,*/*q=0.8,',
                       'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*; q=0.3',
                       'Accept-Encoding':'gzip',
                       'Connection':'close',
                       'Referer':'http://www.baidu.com/link?url=_andhfsjjjkRgEWkj7i9cFmYYGsisrnm2A-TN3XZ'
                                 'DQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;eqid=c3435a7d00006bd600000003582bfd1f'
                                 }

pdflink_list = []
article_titles_list = []

if not os.path.exists(dir_save + 'pdf_link_list.txt') or not os.path.exists(dir_save + 'article_title_list.txt'):
    response = requests.get(url_paperhome,header)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")
    links = soup.find_all('a',text="pdf")
    article_titles = soup.find_all("div",class_="bibref")
    index = 0

    for link in links:
        # pdfkit.from_url(download_home+link.get('href'),dir_save+)
        pdflink_list.append(download_home+link.get('href'))
        index += 1
    for article_title in article_titles:
        article = article_title.text
        rr = re.compile(r'{(.*?)}')
        article = rr.findall(article)
        # print(article[1])
        article_titles_list.append(article[1])

    with open(dir_save+'pdf_link_list.txt','w+') as f_pdf:
        for link in pdflink_list:
            f_pdf.writelines(link + '\n')
    with open(dir_save+'article_title_list.txt','w+') as title_pdf:
        for title in article_titles_list:
            title_pdf.writelines(title + '\n')
else:
    with io.open(dir_save+'pdf_link_list.txt','r+',encoding='utf8') as f_pdf:
        for link in f_pdf.readlines():
            pdflink_list.append(link.strip())
    with io.open(dir_save+'article_title_list.txt','r+',encoding='utf8') as title_pdf:
        for title in title_pdf.readlines():
            article_titles_list.append(title.strip())

pdflinks_queue = Queue(len(pdflink_list))
article_titles_queue = Queue(len(article_titles_list))


for url,title in zip(pdflink_list,article_titles_list):
    pdflinks_queue.put(url)
    article_titles_queue.put(title)





def fetchUrlandTitle(urlqueue,titlequeue):
    while True:
        try:
            url = urlqueue.get_nowait()
            title = titlequeue.get_nowait()
        except Exception as e:
            break
        try:
            download(url,title)
            time.sleep(1)
        except Exception as e:
            continue

def download(url,title):
    # pdfkit.from_url(url,dir_save+title+".pdf",configuration=config)
    if title.find(":") != -1:
        title = title.replace(":",'-')
    if title.find("/") != -1:
        title = title.replace("/",'-')
    if title.find('<') != -1:
        title = title.replace("<",'-')
    if title.find(">") != -1:
        title = title.replace(">",'-')
    if title.find("?") != -1:
        title = title.replace("?",'-')
    if title.find("|") != -1:
        title = title.replace("|",'-')
    if title.find('"') != -1:
        title = title.replace('"','-')
    if title.find('*') != -1:
        title = title.replace('*','-')

    if not os.path.exists(dir_save+title+".pdf"):
        f = requests.get(url,header)
        print(f.status_code)
        if f.status_code == 200:
            data = f.content
            with open(dir_save+title+".pdf",'wb') as pdf:
                pdf.write(data)



def multiprocess_crawler(max_threads = 10):
    pass


if __name__ == '__main__':
    threads = []
    threadNum = 5
    for i in range(5):
        t = threading.Thread(target=fetchUrlandTitle,args=(pdflinks_queue,article_titles_queue))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("download finished!")