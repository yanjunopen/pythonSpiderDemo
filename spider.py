import urllib
import article
import redis


from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

re = redis.Redis("192.168.46.128", 6379, 0)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_article_list')
def get_article_list():
    url = "http://www.chong4.com.cn"
    response = urllib.request.urlopen(url)
    line = response.read()
    soup = BeautifulSoup(line, "html.parser")
    nodes = soup.select(".textbox-title a")

    for node in nodes:
        ar = article.Article()
        ar.title = node.string
        ar.link = url + node.get("href")
        ar.id = ar.link.split("?")[1]
        re.hmset(ar.id, ar.__dict__)
        get_article_detail(ar.link, ar.id)

    re.save()
    return "ok"


def get_article_detail(url, id):
    response = urllib.request.urlopen(url)
    line = response.read()
    soup = BeautifulSoup(line, "html.parser")

    nodes = soup.select(".textbox-content p")
    name = id + "_content"
    for node in nodes:
        re.rpushx(name, node.string)

    return "ok"

if __name__ == '__main__':
    app.run()

