#!/usr/bin/env python
# coding=utf-8
import pdb
import time 
import random 
from bs4 import BeautifulSoup
from splinter import Browser   
from urllib.parse import urlparse 

def save2file(query,results):
    with open(query,'w') as f:
        for i in results:
            print(i)
            f.write(i+'\n')

def format_url(url):
    if urlparse(url)[2] == '':
        url += '/'
    url_structure = urlparse(url)
    netloc = url_structure[1]
    path = url_structure[2]
    query = url_structure[4]

    temp = (netloc,tuple([len(i) for i in path.split('/')]),tuple(sorted([i.split('=')[0] for i in query.split('&')])))
    return temp

def url_similar_control(urls):
    SIMILAR_SET = set() 
    results = set()
    for url in urls:
        t = format_url(url)
        if t not in SIMILAR_SET:
            SIMILAR_SET.add(t)
            results.add(url) 
    return results


def get_result(query,page):
    google_domains = ['www.google.ad', 'www.google.ae.', 'www.google.com.af', 'www.google.com.ag', 'www.google.am', 'www.google.co.ao', 'www.google.com.ar', 'www.google.as', 'www.google.at', 'www.google.com.au', 'www.google.az', 'www.google.ba', 'www.google.bs', 'www.google.bf', 'www.google.be', 'www.google.bg', 'www.google.bi', 'www.google.bj', 'www.google.com.bo', 'www.google.by', 'www.google.ca', 'www.google.cd', 'www.google.cf', 'www.google.ch', 'www.google.ci', 'www.google.co.ck', 'www.google.cl', 'www.google.cm', 'www.google.co.cr', 'www.google.com.cu', 'www.google.cz', 'www.google.dk', 'www.google.de', 'www.google.dj', 'www.google.com.do', 'www.google.dz', 'www.google.ee', 'www.google.com.ec', 'www.google.com.eg','www.google.es', 'www.google.com.et', 'www.google.fr', 'www.google.fi', 'www.google.com.fj', 'www.google.fm', 'www.google.ga', 'www.google.gg', 'www.google.com.gh', 'www.google.com.gi', 'www.google.gl', 'www.google.gm', 'www.google.gp', 'www.google.gr', 'www.google.com.gt', 'www.google.gy','www.google.hn', 'www.google.hr', 'www.google.ht', 'www.google.hu', 'www.google.co.in', 'www.google.co.id', 'www.google.it', 'www.google.im', 'www.google.is', 'www.google.co.il', 'www.google.co.jp', 'www.google.je', 'www.google.com.jm', 'www.google.jo', 'www.google.ki', 'www.google.co.ke', 'www.google.kg', 'www.google.co.kr', 'www.google.com.kw', 'www.google.kz', 'www.google.la', 'www.google.com.lb', 'www.google.li', 'www.google.lk', 'www.google.co.ls', 'www.google.lt', 'www.google.lu', 'www.google.lv', 'www.google.com.ly', 'www.google.co.ma', 'www.google.md', 'www.google.me', 'www.google.mg', 'www.google.mk', 'www.google.ml', 'www.google.mn', 'www.google.ms', 'www.google.com.mt', 'www.google.mu', 'www.google.mv', 'www.google.mw', 'www.google.com.mx', 'www.google.com.my', 'www.google.co.mz', 'www.google.no', 'www.google.com.na', 'www.google.ne', 'www.google.com.nf', 'www.google.com.ng', 'www.google.ni', 'www.google.nl', 'www.google.com.np', 'www.google.nr', 'www.google.nu', 'www.google.co.nz', 'www.google.com', 'www.google.pt', 'www.google.com.pa', 'www.google.com.pe', 'www.google.com.ph', 'www.google.com.pk', 'www.google.pl', 'www.google.pn', 'www.google.com.pr', 'www.google.ps', 'www.google.com.py', 'www.google.rs', 'www.google.ru', 'www.google.ro', 'www.google.rs', 'www.google.rw', 'www.google.com.sl', 'www.google.si', 'www.google.sc', 'www.google.com.sg', 'www.google.sh', 'www.google.sk', 'www.google.sm', 'www.google.sn', 'www.google.st','www.google.com.sv', 'www.google.com.sb', 'www.google.td', 'www.google.tg', 'www.google.co.th', 'www.google.com.tj', 'www.google.tk', 'www.google.tl', 'www.google.tm', 'www.google.to', 'www.google.com.tr', 'www.google.tt', 'www.google.com.tw', 'www.google.co.tz', 'www.google.com.ua', 'www.google.co.ug', 'www.google.com.uy', 'www.google.co.uz', 'www.google.co.uk', 'www.google.co.ve', 'www.google.vg', 'www.google.co.vi', 'www.google.com.vn', 'www.google.vu', 'www.google.ws', 'www.google.co.zm', 'www.google.co.zw', 'www.google.co.za']
    user_agents = [
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
     'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
      Version/6.0 Mobile/10A5355d Safari/8536.25', \
     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/28.0.1468.0 Safari/537.36', \
     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
]

    subdomains = 'news','translate','calendar','play','drive','plus','photos'
    results = []
    ua = random.choice(user_agents)
    print(ua)
    browser = Browser(user_agent=ua)
    base_url = 'https://{}/search?hl=env&filter=0&num=100&q={}&start={}'
    scroll = 'scrollTo(0,{})'
    for j in ('jp','vn','hk','tw'):
        for i in range(page):
            height = 0
            google_domain = random.choice(google_domains)
            subdomain = random.choice(subdomains) 
            subdomain = 'https://{}.google.com'.format(subdomain)
            url = base_url.format(google_domain,query.format(j),i*100)

            browser.visit(subdomain) 

            if i == 5:
                browser.reload() 
                time.sleep(14)

            for k in range(3):
                rand_int = random.randint(5,10)
                height += rand_int 
                browser.execute_script(scroll.format(height*200))
                time.sleep(rand_int) 

            try:
                browser.visit(url) 
            except Exception as e:
                print(url+' error\n')
                print(e)

            soup = BeautifulSoup(browser.html,'lxml') 

            for k in range(3):
                rand_int = random.randint(2,5) 
                height += rand_int
                browser.execute_script(scroll.format(height*300))
                time.sleep(rand_int)   


            if browser.url.find('ipv4.google.com') != -1:
                i -= 1
                continue

            
            if i in (2,7):
                browser.back() 
                time.sleep(10) 



            h3 = soup.find_all(class_='r')
            results.extend( [i.a['href'] for i in h3])
            browser.cookies.delete() 
            if len(h3) < 10:
                break 

    return results

if __name__=='__main__':
    q = 'ext:action site:{}'
    results = get_result(q,10)
    results = url_similar_control(results)
    save2file('test',results)
