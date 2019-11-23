import requests
from bs4 import BeautifulSoup
from pprint import pprint


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if vote:
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return hn


def sort_stories_by_vote(hn):
    return sorted(hn, key=lambda x: x['votes'], reverse=True)


def get_data_from_page(page_number):
    res = requests.get(f'https://news.ycombinator.com/news?p={page_number}')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    if links:
        subtext = soup.select('.subtext')
        return create_custom_hn(links, subtext)
    return None


if __name__ == "__main__":
    news = []
    page_number = 1
    while True:
        scraped_data = get_data_from_page(page_number)
        if scraped_data:
            news.extend(scraped_data)
            page_number += 1
        else:
            break

    news = sort_stories_by_vote(news)
    pprint(news)
