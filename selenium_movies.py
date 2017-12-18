import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

print("Initializing driver...")
browser = webdriver.Firefox()  # executable_path='geckodriver.exe')
browser.get('http://o2tvseries.com/Madam-Secretary-8/Season-04/index.html')
elements = browser.find_element_by_class_name(
    'data_list').find_elements_by_xpath("//a[@href]")

print("Populating episode list...")
episodes = []
for element in elements:
    if 'Episode' in element.get_attribute("href"):
        episodes.append(element.get_attribute("href"))

print("Processing redirected urls...")
download_list = []
for episode in episodes:
    per_episode = webdriver.Firefox()  # executable_path='geckodriver.exe')
    print("Episode is:", episode)
    per_episode.get(episode)
    elem_episodes = per_episode.find_element_by_class_name(
        'data_list').find_elements_by_xpath("//a[@href]")
    for elem_episode in elem_episodes:
        if 'HD (TvShows4Mobile.Com).mp4' in elem_episode.text:
            print("ELEM EPI:", elem_episode)
            download_list.append('http://d5.o2tvseries.com/' + 'Madam%20Secretary/' + 'Season%2004/' +
                                 elem_episode.text.replace(' ', '%20'))
            print(elem_episode.get_attribute('href').replace(
                'http', 'https'), elem_episode.text)
    per_episode.close()


for download in download_list:
    episode = download[-38:].replace('%20', ' ')
    r = requests.get(download, allow_redirects=True)
    open(episode, 'wb').write(r.content)
    print('downloaded this Episode : ' + episode)
    break
