import requests
from bs4 import BeautifulSoup
import wikipedia
from wikipedia import exceptions
import google
import sys
import os
from flask import Flask, jsonify, request


# full_argument = " ".join(sys.argv[1:])
# search_query = full_argument

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify('Hello')

@app.route('/summary/<search_query>')
def getSummary(search_query):
    try:
        topic_summary = wikipedia.page(search_query).summary
        return jsonify({'summary': topic_summary})

    except exceptions.DisambiguationError as e:
        return jsonify(e)



# YOUTUBE SEARCHES

@app.route('/youtube/<search_query>')
def getYoutube(search_query):
    r = requests.get('https://www.youtube.com/results?search_query=' + search_query)

    html_text = r.text

    soup = BeautifulSoup(html_text, 'html.parser')

    hrefs = soup.find_all('a')

    youtube_links = []
    youtube_home_link = 'https://www.youtube.com'

    for link in hrefs:
        if '/watch' in link.get('href'):
            total_link = "%s%s" % (youtube_home_link, link.get('href'))
            youtube_links.append(total_link)

    return jsonify({'youtube links': youtube_links})



#WIKIPEDIA SEARCHES

@app.route('/wikipedia/<search_query>')
def getWikipedia(search_query):
    try:
        wikipedia_page = wikipedia.page(search_query)
        wikipedia_link = wikipedia_page.url
        return jsonify({'wikipedia': wikipedia_link})


    except wikipedia.WikipediaException:
        return jsonify('Page not available')
    except exceptions.DisambiguationError:
        return jsonify('There are multiple wikipedia pages')




# NEW YORK TIMES
@app.route('/new_york_times/<search_query>')
def getNYT(search_query):
    nyt_articles = []

    payload = {'api-key': '452985148bfb426e8815fc9841e5b58c', 'q': search_query, 'begin_date': '20150101'}
    nyt_search = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json', params=payload)
    nyt_response = nyt_search.json()['response']['docs']

    for article in nyt_response:
        nyt_articles.append(article['web_url'])

    return jsonify({'new york times': nyt_articles})



#Britanica Search Results
@app.route('/britannica/<search_query>')
def getBritannica(search_query):
    britannica_home_url = 'https://www.britannica.com'

    britannica_links = []

    britannica_search = requests.get('https://www.britannica.com/search?query=' + search_query)
    britannica_soup = BeautifulSoup(britannica_search.text, 'html.parser')
    britannica_search_results = britannica_soup.find_all('li', 'sr-result')

    for result in britannica_search_results:
        full_britannica_link = '%s%s' % (britannica_home_url, result.a['href'])
        britannica_links.append(full_britannica_link)
    return jsonify({'britannica': britannica_links})



#GOOGLE
@app.route('/google/<search_query>')
def getGoogle(search_query):
    google_top_20 = []
    google_results = google.search(search_query, num=20, stop=1)

    for result in google_results:
        google_top_20.append(result)

    return  jsonify({'google': google_top_20})


#Reference.com

@app.route('/reference/<search_query>')
def getReference(search_query):

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

    return jsonify({'reference': reference_links})



@app.route('/patents/<search_query>')
def getPatents(search_query):
    patents = requests.get('http://www.patentsview.org/api/patents/query?q={%22_text_all%22:{%22patent_title%22:"' + search_query + '"}}')
    patents = patents.json()['patents']
    google_patent_base = 'http://www.google.ca/patents/US'
    patent_links = []
    for patent in patents:
        google_link = ('%s%s' % (google_patent_base, patent['patent_number']))
        patent_links.append({'link': google_link, 'title': patent['patent_title']})

    return jsonify({'patents': patent_links})


# print('TOPIC SUMARRY ---------------------------------')
# print(topic_summary)
# print('YOUTUBE ---------------------------------')
# print(youtube_links)
# print('WIKIPEDIA ---------------------------------')
# print(wikipedia_link)
# print('NYT ---------------------------------')
# print(nyt_articles)
# print('BRITANNICA ---------------------------------')
# print(britannica_links)
# print('GOOGLE ---------------------------------')
# print(google_top_20)
# print('REFERENCE ---------------------------------')
# print(reference_links)





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)