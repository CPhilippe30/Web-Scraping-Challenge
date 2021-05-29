# import dependencies
from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# This is for debugging

def savetofile(contents):
    file = open('_temporary.txt',"w",encoding="utf-8")
    file.write(contents)
    file.close()


def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News

    #Scrape the Mars News Site and collect the latest News Title and Paragraph Text.
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    news = soup.find('div', class_="list_text")
    news_title = news.text
    news_paragraph = news.find('div',class_="article_teaser_body").text

    print(f"Latest News Title: {news_title}")
    print(f"Latest News Paragraph: {news_paragraph}")
    

    ## JPL Mars Space Images - Featured Image

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    space_image = soup.find('img', class_="headerimage fade-in")['src']
    img_url = space_image.replace("background-image: url('","").replace("');","")
    featured_image_url = f"https://spaceimages-mars.com/{img_url}"


    # Mars facts

    #Launch Website and Parses Data into Beautiful Soup.
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    facts_df = tables[0]
    facts_df.columns = ['Fact', 'Value']
    facts_df['Fact'] = facts_df['Fact'].str.replace(':', '')

    facts_df = tables[0]
    facts_df.columns = ['Fact', 'Value']
    facts_df['Fact'] = facts_df['Fact'].str.replace(':', '')

    facts_html = facts_df.to_html()

    #Use Pandas to convert the data to a HTML table string.
    html_table = (facts_df.to_html()).replace('\n', '')
    html_table


        
    # Mars Hemispheres

    #Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
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
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        oneurl = base_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(oneurl)


    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    
    marspage = {}
    marspage["news_test"] = news_title
    marspage["news_find"] = news_paragraph 
    marspage["featured_image_url"] = featured_image_url
    marspage["marsfacts_html"] = facts_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
    
