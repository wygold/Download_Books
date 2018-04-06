# coding: utf-8
import requests
from bs4 import BeautifulSoup
import json
import re
import xml.etree.ElementTree as ET
import operator
from collections import OrderedDict
from book import Book


def search_book(bookname):
    url = 'https://content.googleapis.com/customsearch/v1?'
    payload = {
        'key' : 'AIzaSyDR9xsxHcem0B-HyaOZ9pOLeKsBCluD9N0',
        'cx':'004126777754148953309:ebpsbzqi5le',
        'q': bookname
        }

    headers ={}
    cookies = {}

    r = requests.get(url, headers=headers, params=payload, cookies=cookies, timeout=5)

    #print r.url

    soup = BeautifulSoup(r.content,'html.parser')

    json_result = json.loads(str(soup))
    if len(json_result['items']) > 0:
        this_book = Book()
        this_book.book_name = bookname
        this_book.book_url = json_result['items'][0]['formattedUrl']
        print this_book.book_url
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
    page_details = OrderedDict()

    for chapter in soup.find_all(target='_blank'):
        if 'b/'+str(book_number) in chapter['href']:
            page_key = int(str(chapter['href']).split('/')[-1].split('.')[0])
            page_url = chapter['href']
            page_title = chapter.text
            page_details[page_key]=[page_url,page_title]

    page_details=OrderedDict(sorted(page_details.items(),key=lambda t:t[0]))

    book_content = ''

    for key , value in page_details.iteritems():
        actual_page_url = url+str(re.split("/",value[0])[-1])
        print 'Download book chapter url: ' + actual_page_url
        book_content = book_content + get_one_page(actual_page_url)

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


def update_book(book):
    pass

def monitor_book(book):
    pass

def email_updated_page(book):
    pass

bookname = u'诡秘之主'
searched_book = search_book(bookname)
book_content = download_book(bookname, searched_book.book_url)
dump_book(bookname, book_content)


