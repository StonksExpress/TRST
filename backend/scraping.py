from bs4 import BeautifulSoup
import sys
import requests

def scraping(websiteName):
    response = requests.get(websiteName)
    soup = BeautifulSoup(response.content, "html.parser")
    elements=[]

    for a in soup.findAll('div',attrs={'jscontroller':'d0DtYd'}):
        title=a.find('a', attrs={'class':'DY5T1d'})
        newssite=a.find('a', attrs={'class':'wEwyrc AVN2gc uQIVzc Sksgp'})
        date=a.find('time')

        el=[title,newssite,date]
        elements.append(el)

    elements_print(elements)
    return elements

def elements_print(elements):
    for el in elements:
        for a in el:
            print(a.text)
        print('\n')


websiteName = sys.argv[1]
elements = scraping(websiteName)
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
