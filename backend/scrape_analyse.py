from bs4 import BeautifulSoup
from newspaper import Article
import requests
from string import printable
import re
import nltk
import time

def scrapeAnalyse(url, isGeneral, keywords):
    nltk.download('punkt')
    if(isGeneral):
        all_data=[]
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        # ------ Google News ------
        response = requests.get("https://news.google.com/search?q=" + keywords, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for index, link in enumerate(soup.findAll('div', attrs={'class':'NiLAwe'})):
            if index >= 5:
                break
            children = link.findChildren('a', recursive=False)
            for child in children:
                news_url = child.get('href')
                article = Article("https://www.news.google.com" + news_url[1:])
                article.download()
                article.parse()
                date = None
                if article.publish_date == None:
                    date = time.time()
                else:
                    date = article.publish_date.timestamp()
                el = {"text": article.text, "date": date, "url": "https://www.news.google.com" + news_url[1:]}
                all_data.append(el)

        # ------ Yahoo News ------
        # response = requests.get("https://news.search.yahoo.com/search?p=" + keywords, headers=headers)
        # soup = BeautifulSoup(response.content, "html.parser")

        # for index, link in enumerate(soup.findAll('h4', attrs={'class':'fz-16 lh-20'})):
        #     if index >= 0:
        #         break
        #     children = link.findChildren('a', recursive=False)
        #     for child in children:
        #         news_url = re.sub("\/RV=2.*", "", child.get('href'))
        #         article = Article(news_url)
        #         article.download()
        #         article.parse()
        #         el = {"text": article.text, "date": article.publish_date, "url": news_url}
        #         all_data.append(el)

        # ------ Bing News ------
        response = requests.get("https://www.bing.com/news/search?q=" + keywords, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for index, link in enumerate(soup.findAll('div', attrs={'class':'news-card newsitem cardcommon'})):
            if index >= 5:
                break
            news_url = link.get('url')
            article = Article(news_url)
            article.download()
            article.parse()
            date = None
            if article.publish_date == None:
                date = time.time()
            else:
                date = article.publish_date.timestamp()
            el = {"text": article.text, "date": date, "url": news_url}
            all_data.append(el)

        # all_text = "".join(all_text)
        # all_text = "".join(x for x in all_text if x in printable)
        return all_data

    else:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        keywords = article.keywords
        date = None
        if article.publish_date == None:
            date = time.time()
        else:
            date = article.publish_date.timestamp()
        return (article.text, "+".join(keywords), date)

# my_data = scrapeAnalyse(None, True, "ciara+storm")
# for el in my_data:
#     print("----- ELEMENT -----")
#     print(el["date"])
#     print(el["url"])
#     print(el["text"])
#     print("\n")
