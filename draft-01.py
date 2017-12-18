import sys
print("Executing {0}".format(sys.argv[0]))
print("Importing libraries...")
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

print("Initializing driver...")
browser = webdriver.Firefox()  # executable_path='geckodriver.exe')
#ms4 = 'http://o2tvseries.com/Madam-Secretary-8/Season-04/index.html'
#got7 = 'http://o2tvseries.com/Game-of-Thrones-8/Season-07/index.html'
scandal = 'http://o2tvseries.com/Scandal-8/Season-07/index.html'
root_dir = 'http://d7.o2tvseries.com/Scandal/Season%2007/'

print("Downloading webpage...")
browser.get(scandal)
elements = browser.find_element_by_class_name(
    'data_list').find_elements_by_xpath("//a[@href]")

print("Finding episodes...")
episodes = []
for element in elements:
    if 'Episode' in element.get_attribute("href"):
        episodes.append(element.get_attribute("href"))
episodes.reverse()
print("Found...{}!".format(len(episodes)))

download_list = []
print("Finding download links...")
for episode in episodes:
    per_episode = webdriver.Firefox()  # executable_path='geckodriver.exe')
    per_episode.get(episode)
    elem_episodes = per_episode.find_element_by_class_name(
        'data_list').find_elements_by_xpath("//a[@href]")
    for elem_episode in elem_episodes:
        if 'HD (TvShows4Mobile.Com).mp4' in elem_episode.text:
            downlink = root_dir + elem_episode.text.replace(' ', '%20')
            download_list.append(downlink)
    per_episode.close()
print("found...({0})!".format(len(download_list)))

count = 1
for download in download_list:
    print('Downloading episode {0}, {1} remaining...'.format(
        count, len(download_list) - count))
    print("Source:", download)
    episode = download[-38:].replace('%20', ' ')
    print('Destination:', episode)
    print("GET.")
    r = requests.get(download, allow_redirects=True)
    print("WRITE")
    open(episode, 'wb').write(r.content)
    print("Done.")
    count += 1
