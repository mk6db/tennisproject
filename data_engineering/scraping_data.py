import requests
import re
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

class GitHubDataScrape(object):
    '''Class get links from a main GitHub Page & then dowloads data from GitHub'''

    def __init__(self):
        self.links = []
        self.links_prefix = 'https://raw.githubusercontent.com'

    def get_data_links(self, mainpage_url, link_includes=None):
        page = requests.get(mainpage_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links_prep = soup.findAll('a', class_='js-navigation-open')

        links_temp = [link.get('href') for link in links_prep]
        if link_includes:
            links_temp = [l for l in links_temp if link_includes in l]
        links_temp = [l.replace('blob/','') for l in links_temp]
        self.links.extend(links_temp)

        return self.links

    def download_data(self, save_path):
        for link in self.links:
            time.sleep(random.randint(10,20))
            data_page = requests.get(self.links_prefix + link)
            data = data_page.content.decode('utf-8')
            data = pd.DataFrame([x.split(',') for x in data.split('\n')][1:],
                                 columns=[x.split(',') for x in data.split('\n')][0])
            file_name = link.split('/')[-1]
            data.to_csv(save_path + '/' + file_name)

if __name__ == '__main__':
    GHData = GitHubDataScrape()
    GHData.get_data_links('https://github.com/JeffSackmann/tennis_atp', 
                          link_includes='atp_')
    GHData.download_data('../data/raw_data')
