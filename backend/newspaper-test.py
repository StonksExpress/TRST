from newspaper import Article

url = "https://www.bbc.co.uk/news/uk-51425482"
article = Article(url)

article.download()
print(article.html)

article.parse()
print(article.authors)
print(article.publish_date)
print(article.text)
