# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pdb


def scrape_all():
    # Initiate headless driver for deployment
    # Set up Splinter (prepping our automated browser and specifying chrome as the browser)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_url_title": hem_data(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    #print('------------------------------------------------------------------------------------------------------------------------------')
    try:
        #use read_html to scrape the facts table into a datafrane
        #print('-------################################################################################################--------------------')
        df = pd.read_html('https://galaxyfacts-mars.com')[0] # asking pandas read to get the first table it encounters and store it as a df
        #pdb.set_trace()

    except BaseException as e:
        print(e)
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # pdb.set_trace()
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html() 

def hem_data(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soups = soup(html, 'html.parser')

    hemisphere_image_urls = []

    for i in range(4):
    #create empty dictionary
        hemispheres = {}
        
        #navigating page
        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.find_link_by_text('Sample').first
        
        #getting images and titles
        # print("AA")
        img_url = sample['href']
        title = browser.find_by_css("h2.title").text
        # print("BB")
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        
        #adding dictionary and resetting bowerser to previous page
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
