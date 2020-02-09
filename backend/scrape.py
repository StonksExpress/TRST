from bs4 import BeautifulSoup
import sys
import requests
import re
import newspaper import Article

def scrape(websiteName):
    response = requests.get(websiteName)
    soup = BeautifulSoup(response.content, "html.parser")
    elements=[]

    if websiteName == "https://www.news.google.com":
        print("google")
        main_tag = 'div'
        main_attrs = {'jscontroller':'d0DtYd'}
        title_tag = 'a'
        title_attrs = {'class':'DY5T1d'}
        newssite_tag = 'a'
        newssite_attrs = {'class':'wEwyrc AVN2gc uQIVzc Sksgp'}
        date_tag = 'time'
    elif websiteName == "https://uk.news.yahoo.com":
        print("yahoo")
        main_tag = 'div'
        main_attrs = {'class':'Ov(h) Pend(44px) Pstart(25px)'}
        title_tag = 'a'
        title_attrs = {'class':'Fw(b) Fz(20px) Lh(23px) Fz(17px)--sm1024 Lh(19px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'}
        newssite_tag = 'div'
        newssite_attrs = {'class':'C(#959595) Fz(11px) D(ib) Mb(6px)'}
        date_tag = 'div'
    elif websiteName == "https://www.bing.com/news":
        print("bing")
        main_tag = 'div'
        main_attrs = {'class':'caption'}
        title_tag = 'a'
        title_attrs = {'class':'title'}
        newssite_tag = 'a'
        newssite_attrs = {'aria-label':re.compile('Search news from .*')}
        date_tag = 'span'
    else:
        print("not predefined website")
        article = Article(websiteName)
        article.download()
        for a in soup.findAll('p'):
            elements.append(a.text)
        return elements


    # with open("temp.txt", 'w') as file:
    #     file.write(soup.prettify().encode('utf-8'))
    #print(soup.prettify())

    for a in soup.findAll(main_tag, attrs=main_attrs):
        #print("in findAll loop")
        title=a.find(title_tag, attrs=title_attrs).text
        newssite=a.find(newssite_tag, attrs=newssite_attrs).text
        date=a.find(date_tag).text

        el={"title": title, "newssite": newssite, "date": date}
        elements.append(el)

    return elements

def elements_print(elements):
    for el in elements:
        if isinstance(el, dict): # for predefined websites
            print(el["title"])
            print(el["newssite"])
            print(el["date"])
            print('\n')
        else: # for not predefined websites
            print(el)


websiteName = sys.argv[1]
elements = scrape(websiteName)
elements_print(elements)

#headline = driver.find_element_by_class_name('fc-container--rolled-up-hide fc-container body')

'''
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("joff")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
#driver.close()
'''


#headline = driver.find_element_by_xpath("/html/body/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[2]")
#print(headline)
#print(soup.get_text())
#for a in soup.findAll('div',attrs={'class':'lBwEZb BL5WZb xP6mwf'}):
#for a in soup.findAll('div',attrs={'class':'NiLAwe mi8Lec  gAl5If jVwmLb Oc0wGc R7GTQ keNKEd j7vNaf nID9nc'}):


#print(products)
# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
# df.to_csv('products.csv', index=False, encoding='utf-8')
