import re

import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self):
        self.rbc = self.rbc()
        self.yandex = self.yandex()
        self.vedomosti = self.vedomosti()
        self.kommersant = self.kommersant()

    def yandex(self):
        url = 'https://yandex.ru'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = {}
        for link in soup.find_all('a',
                                  class_='home-link list__item-content list__item-content_with-icon home-link_black_yes'):
            result[link['href']] = link.text
        return result

    def kommersant(self):
        url = 'https://www.kommersant.ru/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = {}
        for link in soup.find_all('li', class_='b-newsline__item b-newsline__item--news-of-the-day'):
            for line in link.find_all('a'):
                result["https://kommersant.ru" + line['href']] = line.text
        return result

    def vedomosti(self):
        url = 'https://www.vedomosti.ru/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = {}
        for link in soup.find_all('a', class_=re.compile("articles-cards-list__card card-article")):
            for line in link.find_all('span', class_='card-article__title'):
                result["https://vedomosti.ru" + link['href']] = line.text
        return result

    def rbc(self):
        url = 'https://www.rbc.ru/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = {}
        for link in soup.find_all('a', class_="main__feed__link js-yandex-counter"):
            for line in link.find_all('span', class_='main__feed__title'):
                result[link['href']] = line.text
        return result
