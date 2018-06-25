# -*- coding:utf-8 -*-

import re
from PyPDF2 import PdfFileMerger, PdfFileReader
from bs4 import BeautifulSoup
import pdfkit
import requests
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'xt'

url_collection = r"https://www.zhihu.com/collection/189xxx048"
dir_save =  r'save\\'
dir_save_html = dir_save + r'html\\'
dir_save_pdf = dir_save + r'pdf\\'

headers1 = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        "Referer": "https://www.zhihu.com/signin?next=%2Fcollection%2F189001048",
        'Host': 'www.zhihu.com',
        }

#模拟浏览器请求,从浏览器开发者工具获取headers
headers2 = {
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    "cookie" : 'l_n_c=1; q_c1=a7917f7373054f6b8cbfa347febf9036|1529827342000|1529827342000; n_c=1;'
               ' _xsrf=5f3697626c0f470ad7d8ec92f302c68d;'
               ' d_c0="APCleNtHzA2PThQ6qunniVfYZviZm0p0WBA=|1529827344";'
               ' __utma=51854390.1620701759.1529827344.1529827344.1529827344.1; '
               '__utmb=51854390.0.10.1529827344;'
               ' __utmc=51854390;'
               ' __utmz=51854390.1529827344.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/collection/189001048;'
               ' _zap=b07db591-9a43-431c-9d20-9a0a4cd788d5; tgw_l7_route=ec452307db92a7f0fdb158e41da8e5d8;'
               ' l_cap_id="ZTQ0MzNmNTk5NWJmNDdkZTk5N2Q1YzRjM2QzODEwMGY=|1529829874|93f94d90a6bd17c4ff00cc629e5f195ec2fd15b8"; '
               'r_cap_id="MTNmYTBlNzMwOGE0NDU1OTk0OGE5MDVhZDJjODNhMmI=|1529829874|0bb560acd5d3f7ea5c03153417ab09e1c0a25490"; '
               'cap_id="OWExMjNlZDBmMjNlNGMzYWE2Zjg4MGJhMmMwZDU4ZjI=|1529829874|432c721fdfa75e3840af0884be9d51156df739ad"; __utmv=51854390.000--|2=registration_date=20170108=1^3=entry_date=20180624=1;'
               ' capsion_ticket="2|1:0|10:1529829897|14:capsion_ticket|44:N2M2Nzg0NjZlZmI2NDM3YWFmMzEzYmYzYzNhMWJkNTI=|5e0bdd06a3303a25dd9fe88b7e06e188b0dfa7d417ce2b12f313301b27a03bfc"; '
               'z_c0="2|1:0|10:1529829968|4:z_c0|92:Mi4xbGRMbkF3QUFBQUFBOEtWNDIwZk1EU1lBQUFCZ0FsVk5VS2djWEFDTkJHSWtNa3JRdHhYNWV0Nk95RHpoNWNlY05n|2aeec4c449a34bd6fd08ebdc66709176467fb4d1edcdde186812277f99bc3bf3"',
    "referer":'https://www.zhihu.com/signin?next=%2Fcollection%2F189001048',
    "upgrade-insecure-requests": '1',
    "user-agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
def get_urls():
    url_list = []
    for i in range(17):
        url = url + str(i+1)
        url_list.append(url)
    return url_list

def get_html(url_base):
    url_list = []
    title_list = []

    request = requests.get(url_base,headers = headers2)

    soup = BeautifulSoup(request.content,'html.parser')

    tag_span = soup.find_all('span')
    pagelist = []
    for tag in tag_span:
        tag_a = tag.find_all('a',href=re.compile("page"))
        if tag_a != []:
            page = tag_a[0].contents
            pagelist.append(page)

    totalPage = int(pagelist[-2][0])
    if totalPage <= 0:
        return
    f_urllist = open(dir_save+"url_list.txt",'w+')
    f_titlelist = open(dir_save+"title_list.txt",'w+')

    for i in range(totalPage):
        url = url_base + "?page="+ str(i+1)

        request = requests.get(url,headers = headers1)
        html = request.content

        soup = BeautifulSoup(html,"html.parser")
        url_per_page = soup.find_all('h2',class_="zm-item-title")

        for link in url_per_page:
            tag = link.find('a')

            if tag is not None:
                url = tag.get('href')
                if url is not None:
                    name = link.text
                    url_list.append(url)
                    title_list.append(name)
                    print(name)
                    f_urllist.write(url+'\n')
                    f_titlelist.write(name+'\n')
    f_urllist.close()
    f_titlelist.close()
    return url_list,title_list


def save_pdf_from_htmlfile():
    """
    把所有html文件转换成pdf文件
    """
    options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.45in',
    'margin-bottom': '0.75in',
    'margin-left': '0.45in',
    'encoding': "UTF-8",
    'custom-header': [
      ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
      ('cookie-name1', 'cookie-value1'),
      ('cookie-name2', 'cookie-value2'),
    ],
    'outline-depth': 10,
  }
    path_wk = "C:\\soft\\Python27\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf = path_wk)

    count = 0
    for root,dir,filenames in os.walk(dir_save_html):
        for filename in filenames:
            filename = filename.decode('gb2312').encode('utf8')
            save_pdf_filename = dir_save_pdf + filename.rstrip(".html")+ ".pdf"
            html_name = root+filename
            pdfkit.from_file(html_name, save_pdf_filename, options=options,configuration=config)
            count += 1

def save_pdf_from_url(url,file_name):
    """
    把所有html文件转换成pdf文件
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    path_wk = "C:\\soft\\Python27\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf = path_wk)
    pdfkit.from_url(url, file_name,configuration=config)


def save_html(url_list,title_list):
    count = 1
    for url,title in zip(url_list,title_list):
        url = url.strip()
        title = title.strip()
        if title.find(":") != -1:
            title = title.replace(":",'-')
        if title.find("/") != -1:
            title = title.replace("/",'-')
        if title.find(r"\\") != -1:
            title = title.replace("\\",'-')
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

        if url.find('https://') != -1:
            # save_pdf_filename = dir_save_pdf + str(count) + ".pdf"
            # save_pdf_from_url(url,save_pdf_filename)
            if not os.path.exists(dir_save_html+str(count)+".html"):
                f = requests.get(url,headers=headers2)
                data = f.content

                soup = BeautifulSoup(data,'html.parser')
                tag_img = soup.find_all('img')
                for tag in tag_img:
                    src = tag.get('src')
                    actualsrc = tag.get('data-actualsrc')   #文章中真正的img链接在data-actualsrc中，而不是src，坑！

                    if actualsrc is not None:
                        tag['src'] = actualsrc
                print(title)

                title  = dir_save_html + str(count) + '.html'
                utitle = unicode(title,'utf8')
                # print(utitle.decode())
                with open(utitle,'w+') as html:
                    html.write(soup.prettify()) #输出格式化的soup
            count +=1


def merge_pdf(dir,titlelist):
    pdf_manage = PdfFileMerger()
    for root,dir,filenames in os.walk(dir):
        filenames_sorted = sorted(filenames,key=lambda i:int(re.match(r'(\d+)',i).group()))
        merge_page_count = 0
        for filename,title in zip(filenames_sorted,title_list):
            file = root + filename
            f_input = PdfFileReader(open(file,'rb'))
            pdf_manage.append(f_input)
            pdf_manage.addBookmark(title,merge_page_count)  #添加标签
            title_page_count = f_input.getNumPages()
            merge_page_count += title_page_count
        f_output = open(dir_save_pdf+'merge.pdf','wb')
        pdf_manage.write(f_output)

if __name__ == '__main__':
    if not os.path.exists(dir_save+"url_list.txt") or not os.path.exists(dir_save+'title_list.txt'):
        url_list,title_list = get_html(url_collection)
    else:
        with open(dir_save+"url_list.txt",'rb') as f_urllist:
            url_list = f_urllist.readlines()
        with open(dir_save+"title_list.txt",'rb') as f_titlelist:
            title_list = f_titlelist.readlines()

    save_html(url_list,title_list)
    save_pdf_from_htmlfile()
    merge_pdf(dir_save_pdf,title_list)





