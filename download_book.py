# coding: utf-8
import requests
from bs4 import BeautifulSoup
import json
import re
import xml.etree.ElementTree as ET
from book import Book

def search_book(bookname):
    url = 'https://www.googleapis.com/customsearch/v1element'
    payload = {
        'key' : 'AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY',
        'num':'1',
        'hl':'zh_CN',
        'cx':'004126777754148953309:ebpsbzqi5le',
        'q': bookname,
        'cse_tok':'ABPF6Hg1cVl9gzESFzu_qB8L1T5fuhjLiA:1522749215678'
        }

    headers ={}
    cookies = {}

    r = requests.get(url, headers=headers, params=payload, cookies=cookies)

    soup = BeautifulSoup(r.content,'html.parser')

    json_result = json.loads(str(soup))
    if len(json_result['results']) > 0:
        this_book = Book()
        this_book.book_name = bookname
        this_book.book_url = json_result['results'][0]['url']

        r = requests.get(this_book.book_url )
        soup = BeautifulSoup(r.text, 'html.parser')

        # get author info
        this_book.book_author = soup.find('h2').find('a').text

        return this_book



def download_book(bookname, url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    url_parer = re.split("/",url)

    book_number = url_parer[-2]

    #get all page urls
    page_urls = []

    for chapter in soup.find_all(target='_blank'):
        if 'b/'+str(book_number) in chapter['href']:
            if chapter['href'] not in page_urls:
                page_urls.append(chapter['href'])

    page_urls = sorted(page_urls)

    book_content = ''

    for page_url in page_urls:
        actual_page_url = url+str(re.split("/",page_url)[-1])
        #book_content = book_content + get_one_page(actual_page_url)

    return book_content

def get_one_page(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    page_content = ''

    content_flag = False

    title = ET.fromstring(str(soup.find('h1',id='timu')))

    for line in re.split(' ', soup.text):
        if u'恢复默认' in line:
            content_flag = True
        elif u'如果喜欢《' in line :
            content_flag = False
        elif content_flag == True:
            page_content = page_content + line.rstrip()

    page_content = process_book_content(page_content)

    return title.text + page_content + "\n"

def process_book_content(content):
    ##remove unncessary data
    ##replace space with carriage return
    return content.replace('(adsbygoogle=window.adsbygoogle||[]).push({});','').\
        replace(u'　　','\n\n').\
        replace(u'    ','\n\n')


def dump_book(bookname, conent):
    f = open(bookname+'.txt','w+')
    f.write(conent.encode('utf-8'))
    f.close()


def update_book(url):
    pass

def monitor_book(url):
    pass

bookname = u'诡秘之主'
searched_book = search_book(bookname)
book_content = download_book(bookname, searched_book.book_url)
dump_book(bookname, book_content)
