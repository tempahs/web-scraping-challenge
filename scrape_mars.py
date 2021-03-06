#import dependencies
from bs4 import BeautifulSoup
import requests
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

## Defining scrape function that executes all scraping functions below 

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_collection={}
    
    # Retrieve Mars News and store results in a variable
    
    url = 'https://redplanetscience.com'
    browser.visit(url)
    time.sleep(5)    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('section', class_='image_and_description_container')
    queries = results.find_all('div', class_='col-md-12')
    
    # Create lists for news title and texts
    news_heading = []
    news = []
    
    
    for query in queries:
        heading = query.find('div', class_='content_title').text
        news_text = query.find('div', class_='article_teaser_body').text
        news_heading.append(heading)
        news.append(news_text)
        
        
    mars_collection["News_Heading"] = news_heading
    mars_collection["News_Text"] = news
    
    #Mars space Featured image
    
    # URL of the page to be scrapped
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    
    browser.links.find_by_partial_text('FULL IMAGE').click()
    
    # create beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Searching the link for the images
    header = soup.find('div', class_='header')
    result = header.find('div', class_='floating_text_area')
    link = result.find('a')
    href = link['href']
    full_link = url +'/'+ href
    
    mars_collection["Featured_Image"] = full_link
        
        ## Mars facts
    # Use pandas 'read_html' function to scrape all tabular data from a page
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    
    # Pandas dataframe    
    mars_facts_df = tables[0]
    
    # Transforming dataframe to html
    mars_facts_html = mars_facts_df.to_html()
    html_table=mars_facts_html.replace("\n", "")
    
    mars_collection["Facts"] = html_table
    
        ## Mars Hemisphere
    # Creating dictionary for hemisphere images
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    # Loop: Use splinter to navigate to each hemisphere page and create dictionary with image title and url (full res)

    pictures_list = []
    hemispheres = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", 
                   "Syrtis Major Hemisphere Enhanced","Valles Marineris Hemisphere Enhanced"]
    for hemisphere in hemispheres:
        html = browser.html
        browser.links.find_by_partial_text(hemisphere).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', class_='downloads')
        image = result.find_all('li')
        link = image[0]
        a_tag = link.find('a')
        href = a_tag['href']
        full_url = url+href
        dict = {"title": hemisphere, "image_url": full_url}
        pictures_list.append(dict)
        browser.links.find_by_partial_text("Back").click()

    
    mars_collection["Hemispheres"] = pictures_list
    browser.quit()
    
    return mars_collection