import requests
from bs4 import BeautifulSoup
import pprint

# response (to grab first 3 pages 3 urls)
res1 = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
res3 = requests.get('https://news.ycombinator.com/news?p=3')

# parse the string into soup object
soup1 = BeautifulSoup(res1.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
soup3 = BeautifulSoup(res3.text, 'html.parser')

# selectors
soup_list = [soup1, soup2, soup3]
links = []
subtext = []
for soup in soup_list:
    links = links + soup.select('.storylink')
    subtext = subtext + soup.select('.subtext')

# sort the stories by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote) != 0:
            points = int(vote[0].getText().replace(' points', ''))
            # print(points)
            if points > 99: 
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(links, subtext))