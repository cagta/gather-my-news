#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup

"""
    This function get's raw html for further processing.

    @param prefix: http or https
    @param host: host of the resource
    @param postfix: full path of the resource on host

    @return html of the provided resource
"""
def get_html(prefix, host, postfix):
    url = prefix + host
    html = urllib.request.urlopen(url+postfix).read()
    return html

"""
    This funciton writes outputs to the file.

    @param filepath
    @article_list list of the found articles

    @return True if operation is error free otherwise False.
"""
def write_to_file(filepath, article_list, has_statistics):
    try:
        with open(filepath, 'w') as f:
            if(has_statistics):
                for item in article_list:
                    f.write("%s\n" % item['url'])
                    f.write("%s %s likes %s comments\n" % (item['statistics']))
                    f.write("-"*40+"\n")
            else:
                for item in article_list:
                    f.write("%s\n" % item['url'])
                    f.write("-"*40+"\n")
        return True
    except Exception as e:
        print(e)
        return False

"""
    this function gathers most popular articles from dev.to and
    write their urls to a file.

    @param timeframe represents the time should be used as filter
            week, month, year, infinity 
    @return True if operation is error free otherwise False. 
"""
def gather_from_devto(timeframe):
    try:
        prefix = "https://"
        host = "dev.to"
        postfix = "/top/"+timeframe
        url = prefix + host
        html = get_html(prefix, host, postfix)
        

        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.find_all(id='articles-list'))
        article_list = []
        for item in soup.find_all(id='articles-list')[0].find_all('div', 'single-article'):
            if item.find('div', 'reactions-count'):
                likes = item.find('div', 'reactions-count').get_text().strip()
            if item.find('div', 'comments-count') is not None:
                comments = item.find('div', 'comments-count').get_text().strip()
            if item.find('a', 'article-reading-time'):
                time = item.find('a', 'article-reading-time').get_text().strip()
                article_postfix = item.find('a', 'article-reading-time')['href']
            article_list.append({ 'url':url+article_postfix, 'statistics':(time, likes, comments)})

        if article_list and write_to_file('data/'+host+'_articles.txt', article_list, True):
            print('For '+ host + ' outputs can be found at ', 'data/'+host+'_articles.txt')
        else:
            print('No updates for ' + host)
        return True

    except Exception as e:

        print(e)
        return False

"""
    this function gathers reports from weforum.org and 
    write their urls to file. 

    @param howOld how old reports should be considered
            as valid resource
    @param limit how much article should be controlled
    
    @return True if operation is error free otherwise False.
"""
def gather_from_weforum(howOld, limit):
    try:
        prefix = "https://"
        host = "www.weforum.org"
        postfix = "/reports"
        url = prefix + host
        html = get_html(prefix, host, postfix)

        soup = BeautifulSoup(html, 'html.parser')

        article_list= []
        
        for article in soup.find_all('article')[:limit]:
            publish_date = article.find('div','caption').get_text().split('—')[1].strip()
            publish_as_datetime = datetime.strptime(publish_date,"%d %B %Y")
            if ((datetime.today() - publish_as_datetime).days <= howOld):
                article_postfix = article.find('a','tout__link')['href']
                article_list.append({'url': url+article_postfix})

        if article_list and write_to_file('data/'+host+'_articles.txt', article_list, False):
            print('For '+ host + ' outputs can be found at ', 'data/'+host+'_articles.txt')
        else:
            print('No updates for ' + host)
        return True
    except Exception as e:
        print(e)
        return False

#gather_from_devto("week")
gather_from_weforum(20, 10)
