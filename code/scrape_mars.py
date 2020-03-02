#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars - Web Scraping
# #### Submitted by : Sheetal Bongale | UT Data Analysis and Visualization | March 3, 2020

# get_ipython().magic(u'reload_ext lab_black')
import pandas as pd
import pprint
import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from splinter import browser

def scrape():
    # URLs to be scraped:
    NEWS_URL = "https://mars.nasa.gov/news/"
    IMAGE_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    WEATHER_URL = "https://twitter.com/marswxreport?lang=en"
    FACTS_URL = "http://space-facts.com/mars/"
    HEM_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    #### NASA Mars News ####

    # Collect the latest news title from NASA's page and the paragraph teaser text.
    # NEWS_URL = "https://mars.nasa.gov/news/"

    driver = webdriver.Firefox()
    driver.get(NEWS_URL)
    html = driver.page_source

    soup = bs(html, "html.parser")
    news_title = (soup.find("div", class_="list_text")).find("a").text
    # print(f"Latest News Title: {news_title}")
    driver.close()


    teaser_url = (
        "https://mars.nasa.gov/news/" + soup.find("div", class_="list_text").a["href"]
    )
    teaser_url


    r = requests.get(teaser_url)
    html = r.text
    soup = bs(html, "html.parser")
    teaser = soup.find("div", class_="wysiwyg_content").find("p").text
    # print(f"Teaser: {teaser}")


    #### JPL Mars Space Images - Featured Image ####

    # scarpe the JPL web page to scrape the current Featured Mars Image
    # IMAGE_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    driver = webdriver.Firefox()
    driver.get(IMAGE_URL)
    html = driver.page_source
    img_soup = bs(html, "html.parser")

    img_base_url = img_soup.find("article", {"class": "carousel_item"})["style"]

    featured_image_url = re.findall("url\((.*?)\)", img_base_url)[0].replace("'", "")
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    featured_image_title = img_soup.find("h1", class_="media_feature_title").text.strip()
    driver.close()
    # print(f"Image URL: {featured_image_url}")
    # print(f"Image Title: {featured_image_title}")


    #### Mars Weather - Twitter ####

    # scrape the latest Mars weather tweet from the given twitter page
    # WEATHER_URL = "https://twitter.com/marswxreport?lang=en"

    r = requests.get(WEATHER_URL)
    html = r.text
    soup = bs(html, "html.parser")
    mars_weather = soup.find_all("div", class_="js-tweet-text-container")
    mars_weather = mars_weather[0].text
    # print(f"Current Weather on Planet Mars: {mars_weather}")


    #### Mars Facts ####

    #  use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # FACTS_URL = "http://space-facts.com/mars/"

    fact_table = pd.read_html(FACTS_URL)
    mars_fact_table = fact_table[0]

    mars_fact_table.columns = ["Description", "Value"]
    mars_fact_table.set_index("Description", inplace=True)

    # Use Pandas to convert the data to a HTML table string.
    mars_fact_table_html = mars_fact_table.to_html(
        header=False, index=False, justify="left"
    )
    # mars_fact_table_html = mars_fact_table_html.replace("\n", "")
    # print(mars_fact_table_html)


    #### Mars Hemispheres ####

    # scrape to obtain high resolution images for each of Mar's hemispheres.
    # HEM_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    mars_hemispheres = requests.get(HEM_URL).text
    astro_soup = bs(mars_hemispheres, "html.parser")

    hemisphere_dict = []
    hemisphere_dict = [
        {
            "Title": e.text.strip(" Enhanced"),
            "HEM_URL": ("https://astrogeology.usgs.gov" + e["href"]),
        }
        for e in astro_soup.find_all(class_="itemLink product-item")
    ]
        
    # Store all the scrapped data in a dictionary
    mars_dict = {
        "news": news_title,
        "teaser": teaser,
        "image_url": featured_image_url,
        "weather": mars_weather,
        "facts": mars_fact_table_html,
        "hemispheres": hemisphere_dict,
    }
    return mars_dict




