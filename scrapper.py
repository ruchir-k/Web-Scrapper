# building a web scraper

import requests
from bs4 import BeautifulSoup
import pprint
import re

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

# /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/span/a


def get_title(num):
    # /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/span/a
    selector = f'html body center table tr:nth-of-type(3) td table tr:nth-of-type({num}) td:nth-of-type(3) span a'
    elems = soup.select(selector)
    text_parts = [elem.text for elem in elems]
    # /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/span/span[1]
    selector = f'html body center table tr:nth-of-type(3) td table tr:nth-of-type({num+1}) td:nth-of-type(2) span span:nth-of-type(1)'
    scores = soup.select(selector)
    # Extract the text contents of the first element in the `scores` list:
    try:
        score_text = scores[0].text
        # Use a regular expression to extract only the digits from the text:
        digits = re.findall('\d+', score_text)
        score_number = int(digits[0])
    except IndexError:
        score_number = 0

    return text_parts, score_number

def generate_news():
    news = []
    for i in range(1,89,3):
        news.append(get_title(i))
    return sorted(news, key=lambda x: x[1], reverse=True)
    

if __name__ == '__main__':
    news = generate_news()
    pprint.pprint(news)
    # save this to a csv file
    with open('news.csv', 'w') as f:
        f.write('title, website, score\n')
        for item in news:
            f.write(f'{item[0][0]}, {item[0][1]}, {item[1]}\n')


    