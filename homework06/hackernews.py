from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    arguments = str(request.query_string).split('&')
    result =[arguments[0][6:], arguments[1][3:]]
    s.query(News)[int(result[1]) - 1].label = result[0]
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    rows = s.query(News).all()
    info = get_news('https://news.ycombinator.com/newest')
    dict_sql = []
    for identity_sql in rows:
        dict_sql.append({'author': identity_sql.author,
                        'title': identity_sql.title})
    for identity_news in info:
        if {'author': identity_news['author'],
                         'title': identity_news['title']} not in dict_sql:
            news = News(title=identity_news['title'],
                author=identity_news['author'],
                url=identity_news['url'],
                comments=identity_news['comments'],
                points=identity_news['points'])
            s.add(news)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE


if __name__ == "__main__":
    run(host="localhost", port=8080)