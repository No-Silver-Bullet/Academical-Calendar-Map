#! coding:utf8

import requests

from bs4 import BeautifulSoup


class DataTagDecoder(object):
    """
        针对www.aconf.cn上的特定html元素的tag解析器
    """

    def _name(self, tag):
        return tag.find_all('a')[0].get_text()

    def _date(self, tag):

        dstr = tag.find_all('span')[0].get_text().strip()
        pos = dstr.find('~')
        if pos < 0:
            return dstr, dstr
        else:
            bdate = dstr[0:pos]
            edate = bdate[0:-2]+dstr[pos+1:]
            return bdate, edate

    def _pos(self, tag):
        pos = tag.find_all('span')[1].get_text().strip()
        return pos

    def _sponsor(self, tag):
        t = tag.find_all(
            'div', class_="sponsored-row pull-left")
        bpos = str(t).find('\\n')+2
        epos = str(t).find("</div>")-1
        jigou = str(t)[bpos:epos].strip()
        rv = jigou.decode("unicode-escape")
        return rv

    def _subject(self, tag):
        return tag.find_all('a', class_="subject-link")[0].get_text()

    def _reflink(self, tag):
        s = str(tag.find_all('a')[0])
        bpos = s.find('/')
        epos = s.find('"', bpos)
        return "http://www.aconf.cn"+s[bpos:epos]

    def decode(self, tag):
        return {
            "name": self._name(tag),
            "reflink": self._reflink(tag),
            "position": self._pos(tag),
            "bdate": self._date(tag)[0],
            "edate": self._date(tag)[1],
            "spnosor": self._sponsor(tag),
            "subject": self._subject(tag)}


class HtmlDecoder(object):
    """
        针对www.aconf.cn搜索结果页面的解析器
    """

    @staticmethod
    def dataTag(html):
        """
            解析出我们需要的会议数据tag
        """

        htmlobj = BeautifulSoup(html)

        tags = htmlobj.find_all('div', class_="swa-item")

        return tags

    @staticmethod
    def dataHtmlUrl(html):
        """
            搜索结果可能有多页，我们可以解析第一页的html，发现所有结果页的url
        """
        htmlobj = BeautifulSoup(html)
        tag = htmlobj.find_all('ul', class_="pagination")[0]

        tags = tag.find_all('li')

        rv = []
        for tag in tags:
            s = str(tag.a)
            bpos = s.find('/')
            epos = s.find('"', bpos)

            url = "http://www.aconf.cn"+s[bpos:epos]

            rv.append(url)
        return rv[1:]


def test_tagdecorder():

    # url = "http://www.aconf.cn/c.html?date_type=start_date&date_range=&start_date=1514736000&end_date=1514736000"
    # html = requests.get(url)

    html = open("text1.html", 'r')

    decoder = DataTagDecoder()
    for tag in HtmlDecoder.dataTag(html):
        data = decoder.decode(tag)
        for key in data:
            print key, ":", data[key], ", ",
        print ""


def test_htmldecoder():
    url = "http://www.aconf.cn/c.html?date_type=start_date&date_range=&start_date=1524153600&end_date=1524153600"
    html = requests.get(url).text
    HtmlDecoder.dataHtmlUrl(html)


def main():
    test_htmldecoder()


if __name__ == '__main__':
    main()
