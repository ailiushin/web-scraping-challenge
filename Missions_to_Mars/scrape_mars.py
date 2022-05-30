# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

    

# create scrape function
def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo
    mars_data = {}

    #url for NASA's news
    url ="https://redplanetscience.com/"

    # open the url
    browser.visit(url)

    # Let it sleep for 1 second
    time.sleep(1)

    # scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # latest news headline and paragrapgh
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    ### JPL Mars Featured Image

    #url for Mars' image
    jpl_url = 'https://spaceimages-mars.com/'

    # open the jpl_url
    browser.visit(jpl_url)

    # Let it sleep for 1 second
    time.sleep(1)

    # scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find the image
    featured_image_url = soup.find_all('img')[2]["src"]

    #create the url for the image
    image = jpl_url + featured_image_url

    ### Mars Facts

    #url for NASA's mars facts
    facts_url = 'https://galaxyfacts-mars.com/'

    # parse the url
    table = pd.read_html(facts_url)

    # converting to df and renaming columns
    facts = table[0]
    facts.columns=['Description', 'Mars', 'Earth']
    facts = facts.drop([0])

    # converting to html
    fact_table = facts.to_html()
    fact_table.replace('\n','')

    ### Mars Hemispheres
    #url for Mars' Hemispheres
    hems_url = 'https://marshemispheres.com/'

    # open the jpl_url
    browser.visit(hems_url)

    # Let it sleep for 1 second
    time.sleep(1)

    # scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # read to html and extract image urls
    hems_data = soup.find_all("div", class_="item")

    hemisphere_img_urls = []

    # # loop through the data to find title and url info
    # for image in hems_data:
    
    #     title = image.find("h3").text
    
    #     img_url = image.a["href"]
    
    #     url = hems_url + img_url
    
    #     # use requests to get full images url 
    #     response = requests.get(url)
    
    #     # create soup object
    #     soup = bs(response.text,"html.parser")
    
    #     # find full image url
    #     new_url = soup.find("img", class_="wide-image")["src"]
    
    #     # create full image url
    #     full_url = "https://marshemispheres.com/" + new_url
    
    #     # create a dictionary and append to the list before the loop
    #     hemisphere_img_urls.append({"title": title, "img_url": full_url})

    # create mars data dictionary to hold above scraped data
    mars_data = {
        "news_title": news_title,
        "paragraph" : news_p,
        "featured_image_url": image,
        "html_table": fact_table,
        
    }

    # close the browser after scraping
    browser.quit()

    # return our dictionary
    return mars_data
#"hemisphere_img_urls": hemisphere_img_urls