from bs4 import BeautifulSoup
import urllib.request
import re

"""
    this function gathers most popular articles from dev.to and
    write them to a file.

    @param timeframe represents the time should be used as filter
            week, month, year, infinity 
    @return None 
"""
def gather_from_devto(timeframe):
    try:
        prefix = "https://"
        host = "dev.to"
        condition = "/top/week"
        url = prefix + host
        fp = urllib.request.urlopen(url+condition).read()

        soup = BeautifulSoup(fp, 'html.parser')
        #print(soup.find_all(id='articles-list'))
        article_list = []
        for item in soup.find_all(id='articles-list')[0].find_all('div', 'single-article'):
            if item.find('div', 'reactions-count'):
                likes = item.find('div', 'reactions-count').get_text().strip()
            if item.find('div', 'comments-count') is not None:
                comments = item.find('div', 'comments-count').get_text().strip()
            if item.find('a', 'article-reading-time'):
                time = item.find('a', 'article-reading-time').get_text().strip()
                article_url = item.find('a', 'article-reading-time')['href']
            article_list.append({ 'url':url+article_url, 'statistics':(time, likes, comments)})

        with open('data/'+host+'_articles.txt', 'w') as f:
            for item in article_list:
                f.write("%s\n" % item['url'])
                f.write("%s %s likes %s comments\n" % (item['statistics']))
                f.write("-"*40+"\n")
        return 1
    except Exception as e:
        print(e)

gather_from_devto("week")