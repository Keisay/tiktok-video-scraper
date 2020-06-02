from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import urllib.request

# Setting options
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "DuckDuckBot]")

# We use geckodriver because it's better than chromedriver for Tiktok
browser = webdriver.Firefox(profile, executable_path='your_path/geckodriver')
browser.get('the_profile_you_want')

scroll_pause = 1.5
counter=1

# Increase iterations if you want to download more videos
for i in range(5):
    
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    print(counter)
    counter += 1

# We search all videos urls and we put them in a list
element = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]/div/main/div[2]')
hrefs = [x.get_attribute('href') for x in element.find_elements_by_css_selector('a')]

# We create this function to get the video of each url
def getting_video(url):
    browser.set_page_load_timeout(15)
    browser.get(url)
    time.sleep(2)
    try:
        element = browser.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]')
        hover = ActionChains(browser).move_to_element(element).perform()
        link = browser.find_element_by_tag_name('video')
        post = link.get_attribute('src')
        return post
    except NoSuchElementException: # Some links are unavailable so we return a dummy variable
        return 1

# We store all the videos on a new list
empty_list = []
for i in hrefs:
    empty_list.append(getting_video(i))

# We create this function to save the videos
def download_video(url):
    t = datetime.now()
    vid_name = str(t.day) + "." + str(t.month) + "." + str(t.year) + " - " + str(t.hour) + "." + str(t.minute) + "." + str(t.second)
    path = 'in_the_path_you_want'
    full_name = vid_name + ".mp4"
    urllib.request.urlretrieve(url, path+full_name)

# We delete all the dummy variables (1)
for i in empty_list:
    if i == 1:
        empty_list.remove(i)

for i in empty_list:
    download_video(i)
    time.sleep(1.5) # it's important or you won't download all the videos