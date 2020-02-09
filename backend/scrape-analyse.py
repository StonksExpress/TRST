from bs4 import BeautifulSoup
from newspaper import Article
import requests
from string import printable

def scrapeAnalyse(url, isGeneral, keywords):
    if(isGeneral):
        all_text=[]
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
                all_text.append(article.text)

        # ------ Yahoo News ------
        response = requests.get("https://news.search.yahoo.com/search?p=" + keywords, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for index, link in enumerate(soup.findAll('h4', attrs={'class':'fz-16 lh-20'})):
            if index >= 5:
                break
            children = link.findChildren('a', recursive=False)
            for child in children:
                news_url = child.get('href')
                # print(news_url)
                article = Article(news_url)
                article.download()
                article.parse()
                all_text.append(article.text)

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
            all_text.append(article.text)

        all_text = "".join(all_text)
        all_text = "".join(x for x in all_text if x in printable)
        return all_text

    else:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        keywords = article.keywords
        return "+".join(keywords)

my_text = scrapeAnalyse(None, True, "ciara+storm")
print(my_text)
