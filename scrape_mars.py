#!/usr/bin/env python
# coding: utf-8
# Mission to Mars - Web Scraping
# Submitted by : Sheetal Bongale | UT Data Analysis and Visualization | March 3, 2020
######################################################################################

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
    driver.close()

    teaser_url = (
        "https://mars.nasa.gov/news/" + soup.find("div", class_="list_text").a["href"]
    )

    r = requests.get(teaser_url)
    html = r.text
    soup = bs(html, "html.parser")
    teaser = soup.find("div", class_="wysiwyg_content").find("p").text

    #### JPL Mars Space Images - Featured Image ####
    # scarpe the JPL web page to scrape the current Featured Mars Image
    # IMAGE_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    driver = webdriver.Firefox()
    driver.get(IMAGE_URL)
    html = driver.page_source
    img_soup = bs(html, "html.parser")

    img_base_url = img_soup.find("article", {"class": "carousel_item"})["style"]

    featured_image_url = re.findall(r"url\((.*?)\)", img_base_url)[0].replace("'", "")
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    featured_image_title = img_soup.find(
        "h1", class_="media_feature_title"
    ).text.strip()
    driver.close()

    #### Mars Weather - Twitter ####
    # scrape the latest Mars weather tweet from the given twitter page
    # WEATHER_URL = "https://twitter.com/marswxreport?lang=en"

    r = requests.get(WEATHER_URL)
    html = r.text
    weather_soup = bs(html, "html.parser")

    mars_weather = weather_soup.find_all("div", class_="js-tweet-text-container")
    mars_weather = mars_weather[0].text[:-26]

    #### Mars Facts ####
    #  use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # FACTS_URL = "http://space-facts.com/mars/"

    # Use Pandas to read the HTML
    fact_table = pd.read_html(FACTS_URL)
    mars_fact_table = fact_table[0]

    # Convert this facts table to HTML using Pandas
    mars_fact_table_html = mars_fact_table.to_html(
        header=False, index=False, justify="left"
    )

    #### Mars Hemispheres ####
    # scrape to obtain high resolution images for each of Mar's hemispheres.
    # HEM_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    mars_hemispheres = requests.get(HEM_URL).text
    astro_soup = bs(mars_hemispheres, "html.parser")

    hemisphere_dict = []
    hemisphere_dict = [
        {
            "Title": e.text.strip("Enhanced"),
            "hem_img_url": ("https://astrogeology.usgs.gov" + e["href"]),
        }
        for e in astro_soup.find_all(class_="itemLink product-item")
    ]

    # Store all the scrapped data in a dictionary
    mars_dict = {
        "news": news_title,
        "teaser": teaser,
        "featured_image_url": featured_image_url,
        "featured_image_title": featured_image_title,
        "weather": mars_weather,
        "facts": mars_fact_table_html,
        "hemispheres": hemisphere_dict,
        "news_url": NEWS_URL,
        "jpl_url": IMAGE_URL,
        "weather_url": WEATHER_URL,
        "fact_url": FACTS_URL,
        "hemisphere_url": HEM_URL,
    }
    return mars_dict
