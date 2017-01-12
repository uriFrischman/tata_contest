import requests
from bs4 import BeautifulSoup
import wikipedia
from wikipedia import exceptions
import google
import sys


full_argument = " ".join(sys.argv[1:])
search_query = full_argument


try:
    topic_summary = wikipedia.page(search_query).summary

except exceptions.DisambiguationError as e:
    print(e)



# YOUTUBE SEARCHES
r = requests.get('https://www.youtube.com/results?search_query=' + search_query)

html_text = r.text

soup = BeautifulSoup(html_text, 'html.parser')

hrefs = soup.find_all('a')

youtube_links = []
youtube_home_link = 'https://wwww.youtube.com'

for link in hrefs:
    if '/watch' in link.get('href'):
        total_link = "%s%s" % (youtube_home_link, link.get('href'))
        youtube_links.append(total_link)



#WIKIPEDIA SEARCHES

try:
    wikipedia_page = wikipedia.page(search_query)
    wikipedia_link = wikipedia_page.url


except wikipedia.WikipediaException:
    print('Page not available')
except exceptions.DisambiguationError:
    print('There are multiple wikipedia pages')


# NEW YORK TIMES

nyt_articles = []

payload = {'api-key': '452985148bfb426e8815fc9841e5b58c', 'q': search_query, 'begin_date': '20150101'}
nyt_search = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json', params=payload)
nyt_response = nyt_search.json()['response']['docs']

for article in nyt_response:
    nyt_articles.append(article['web_url'])



#Britanica Search Results

britannica_home_url = 'https://www.britannica.com'

britannica_links = []

britannica_search = requests.get('https://www.britannica.com/search?query=' + search_query)
britannica_soup = BeautifulSoup(britannica_search.text, 'html.parser')
britannica_search_results = britannica_soup.find_all('li', 'sr-result')

for result in britannica_search_results:
    full_britannica_link = '%s%s' % (britannica_home_url, result.a['href'])
    britannica_links.append(full_britannica_link)



#GOOGLE

google_top_20 = []
google_results = google.search(search_query, num=20, stop=1)

for result in google_results:
    google_top_20.append(result)



#Reference.com

reference_home_url = 'https://www.reference.com'

reference_links = []

reference_search = requests.get('https://www.reference.com/web?o=600605&l=dir&qo=homepageSearchBox&q=' + search_query)
reference_soup = BeautifulSoup(reference_search.text, 'html.parser')
main_reference_results = reference_soup.find_all('a', {'class': 'PartialCdpArticles-title-link'})
for x in main_reference_results:
    reference_links.append('%s%s' % (reference_home_url, x['href'][19:]))
similar_reference_results = reference_soup.find_all('a', {'class': 'PartialSimilarArticles-title-link'})
for y in similar_reference_results:
    reference_links.append('%s%s' % (reference_home_url, y['href']))




print('TOPIC SUMARRY ---------------------------------')
print(topic_summary)
print('YOUTUBE ---------------------------------')
print(youtube_links)
print('WIKIPEDIA ---------------------------------')
print(wikipedia_link)
print('NYT ---------------------------------')
print(nyt_articles)
print('BRITANNICA ---------------------------------')
print(britannica_links)
print('GOOGLE ---------------------------------')
print(google_top_20)
print('REFERENCE ---------------------------------')
print(reference_links)