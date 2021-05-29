# import dependencies
from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # get variable for the news_title and news_paragraph
    soup = BeautifulSoup(html,'html.parser')
    latest_news_date = (soup.find_all('div', class_="list_date"))[0].get_text()
    latest_news_title = (soup.find_all('div', class_='content_title'))[0].get_text()
    latest_news_paragraph = (soup.find_all('div', class_='article_teaser_body'))[0]
    
    # JPL Mars Space Images - Featured Image

    # scrape for featured image url
    browser.visit('https://spaceimages-mars.com/')


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('img')['src']

    featured_image_url = 'https://spaceimages-mars.com/image/featured/mars3.jpg'


    ## Mars Facts

    ## Scraping Mars Facts Webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tables_df = ((pd.read_html(url))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
    html_table = (tables_df.to_html()).replace('\n', '')
      

  #Visit Website and Parses Data into Beautiful Soup.
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tables_df = ((pd.read_html(facts_url))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])

    #Use Pandas to convert the data to a HTML table string.
    html_table = (tables_df.to_html()).replace('\n', '')    

    #saves the table to an HTML File.
    tables_df.to_html('table.html')



    # Mars Hemispheres

    #Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    items = soup.find_all('div', class_='item')

    urls = []
    titles = []
    for item in items:
        urls.append(base_url + item.find('a')['href'])
        titles.append(item.find('h3').text.strip())

    img_urls = []
    for oneurl in urls:
        browser.visit(oneurl)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        oneurl = base_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(oneurl)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    # Assigning scraped data to a page
    
    marspage = {}
    marspage["Latest News Title"] = latest_news_title
    marspage["Latest News Paragraph"] = latest_news_paragraph
    marspage["featured_image_url"] = featured_image_url
    marspage["marsfacts_html"] = facts_url
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
