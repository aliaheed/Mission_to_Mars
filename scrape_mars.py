# Dependencies
from bs4 import BeautifulSoup
import requests
import os

from splinter import Browser
import time

def get_news():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2019%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    for result in results:
        
        # try:
        title = result.find('div', class_="content_title").text
        para = result.find('div', class_="rollover_description_inner").text
            #para = result.a['href']
            # Identify and return title of listing

            # Identify and return price of listing
            # price = result.a.span.text
            # Identify and return link to listing
            #link = result.a['href']

            # Print results only if title, price, and link are available
    #         if (title and para):
    #             print('-------------')
    #             print(title)
    #             print(para)
    #             #print(link)
        # except AttributeError as e:
        #     return e

    return {"news_title":title,"news_p":para}


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def get_featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # featured_image_url = None
    try:
        browser.visit(url)
        button = browser.find_by_id("full_image")
        button.click()
        time.sleep(2) 
        html_string = browser.html
        soup = BeautifulSoup(html_string, 'html.parser')
        anchor = soup.find('a','ready')
        if anchor.img:
            image_url = anchor.img['src']
        featured_image_url = "https://www.jpl.nasa.gov" + image_url
    except Exception as e:
        print(e)
    return featured_image_url

def get_latest_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html_string = browser.html
    soup = BeautifulSoup(html_string, 'lxml')

    latest_weather = soup.find('div','js-tweet-text-container').text.strip()
    return latest_weather


def get_facts(browser):
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html_string = browser.html
    soup = BeautifulSoup(html_string, 'lxml')
    keys =[]
    values=[]
    table = soup.find('table','tablepress tablepress-id-mars')
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        keys.append(columns[0].text)
        values.append(columns[1].text)
    facts = dict(zip(keys, values))
    return facts

def get_hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)     
    html_string = browser.html
    soup = BeautifulSoup(html_string, 'lxml')
    for header in soup.find_all("h3"):
        title = header.text
        uri = header.find_previous("a")
        image_url = 'https://astrogeology.usgs.gov'+ uri['href'] 
        browser.visit(image_url)

        sub_html_string = browser.html
        sub_soup = BeautifulSoup(sub_html_string, 'lxml')
        image_url='https://astrogeology.usgs.gov' + str(sub_soup.find('img','wide-image')['src'])
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        browser.back()
    return hemisphere_image_urls

def scrape():
    browser = init_browser()

    output = {}
    
    news = get_news()
    
    featured_image_url= get_featured_image(browser)
    
    latest_weather=get_latest_weather(browser)
    
    facts =get_facts(browser)
    
    hemisphere_image_urls =get_hemispheres(browser) 
    
    output ={ "news":news,"featured_image_url":featured_image_url,"weather":latest_weather,"facts":facts, "hemisphere_image_urls":hemisphere_image_urls
    }
    return output

print (scrape())



