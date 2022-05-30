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
    url = 'https://marshemispheres.com/'
    
    # # open the url
    browser.visit(url)

    time.sleep(1)

    # new list to hold titles and images
    hemisphere_img_urls = []

    # loop through the data to find title and url info
    for item in range(4):
        # browse through each article
        browser.links.find_by_partial_text('Hemisphere')[item].click()

        # parse the HTML
        html = browser.html
        hemi_soup = bs(html,'html.parser')

        # scraping
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')

        # store findings into a dictionary and append to list
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_img_urls.append(hemispheres)

        # browse back to repeat
        browser.back()

    # create mars data dictionary to hold above scraped data
    mars_data = {
        "news_title": news_title,
        "paragraph" : news_p,
        "featured_image_url": image,
        "html_table": fact_table,
        "hemisphere_img_urls": hemisphere_img_urls
        }

    # close the browser after scraping
    browser.quit()

    # return our dictionary
    return mars_data