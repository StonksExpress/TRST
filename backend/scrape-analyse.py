from bs4 import BeautifulSoup
from newspaper import Article
import requests

def scrapeAnalyse(url, isGeneral, keywords):
    if(isGeneral):
        # ------ Google News ------
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get("https://news.google.com/search?q=" + keywords, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        all_text=[]

        for index, link in enumerate(soup.findAll('div', attrs={'class':'NiLAwe'})):
            print(index)
            if index >= 10:
                break
            children = link.findChildren('a', recursive=False)
            for child in children:
                news_url = child.get('href')
                article = Article("https://www.news.google.com" + news_url[1:])
                article.download()
                article.parse()
                all_text.append(article.text)

        return all_text

    else:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        keywords = article.keywords
        return "+".join(keywords)

my_text = scrapeAnalyse(None, True, "ciara+storm")
# i = 0
# for el in my_text:
#     print(i)
#     i += 1
#     print(el)
