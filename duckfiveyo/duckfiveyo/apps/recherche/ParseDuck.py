from bs4 import BeautifulSoup
import urllib.request
import re

with urllib.request.urlopen('http://duckduckgo.com/?q=example') as site:
    data = site.read()

parsed = BeautifulSoup(data)
topics = parsed.findAll('div', {'id': 'zero_click_topics'})[0]
results = topics.findAll('div', {'class': re.compile('results_*')})

print(results[0].text)
