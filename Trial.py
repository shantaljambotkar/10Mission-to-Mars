# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

html = browser.html
soups = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.

info_list = soups.find('div', class_='collapsible results')

info_list2 = info_list.find('div', class_='item')
hemisphere_image_urls = []
image =[]
url = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for info in info_list2:
   
    image = info.find('img', class_='thumb').get('scr')
    
   # url = info.find('a')['herf']
     
    print(image)
   # print(url)
   