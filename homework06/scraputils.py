import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news = parser.table.findAll('table')[1].findAll('tr')

    for index in range(30):
        for tbl in range(len(news)):
            if tbl == 0:
                s = news[(index * 3):(index * 3 + 2)][0].text.split()
                if '(' in s[-1]:
                    link = parser.table.findAll('table')[1].findAll('tr')[index * 3].findAll('a', href=True)[1]['href']
                else:
                    link = ''
                list1 = [' '.join(s[1:-1]), link]
            else:
                list2 = []
                if 'points' in news[(index * 3):(index * 3 + 2)][1].text.split() or 'point' in \
                        news[(index * 3):(index * 3 + 2)][1].text.split():
                    list2.append(news[(index * 3):(index * 3 + 2)][1].text.split()[0])
                else:
                    list2.append(0)
                if 'by' in news[(index * 3):(index * 3 + 2)][1].text.split():
                    list2.append(news[(index * 3):(index * 3 + 2)][1].text.split()[news[index * 3 + 1].text.split().index('by') + 1])
                else:
                    list2.append('')
                if 'comments' in news[(index * 3):(index * 3 + 2)][1].text.split() or 'comment' in \
                        news[(index * 3):(index * 3 + 2)][1].text.split():
                    list2.append(int(news[(index * 3):(index * 3 + 2)][1].text.split()[-2]))
                else:
                    list2.append(0)
        stat = {'author': list2[1],
                'comments': list2[2],
                'points': list2[0],
                'title': list1[0],
                'url': list1[1]}
        news_list.append(stat)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    url = parser.table.findAll('table')[1].findAll('a', href=True)

    return url[-1]['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news