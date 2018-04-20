#! coding:utf8

"""
    网页解析相关
"""


import requests
from bs4 import BeautifulSoup


class DataTagDecoder(object):
    """
        针对www.aconf.cn上的特定html元素的tag解析器
    """
    @staticmethod
    def _name(tag):
        return tag.find_all('a')[0].get_text()

    @staticmethod
    def _date(tag):

        dstr = tag.find_all('span')[0].get_text().strip()
        pos = dstr.find('~')
        if pos < 0:
            return dstr, dstr
        else:
            bdate = dstr[0:pos]
            edate = bdate[0:-2]+dstr[pos+1:]
            return bdate, edate

    @staticmethod
    def _pos(tag):
        pos = tag.find_all('span')[1].get_text().strip()
        # print ":", pos.split('\t')[0]

        return pos

    @staticmethod
    def _sponsor(tag):
        t = tag.find_all(
            'div', class_="sponsored-row pull-left")
        bpos = str(t).find('\\n')+2
        epos = str(t).find("</div>")-1
        jigou = str(t)[bpos:epos].strip()

        # i = jigou.find("\n")
        # rv = jigou[0:i]+jigou[i+2:]

        rv = jigou
        rv = jigou.split('\\n')
        if len(rv) > 1:
            x = ""
            for item in rv:
                x += item+','
            rv = x.strip(',')
        else:
            rv = rv[0]
        rv = rv.decode("unicode-escape")

        return rv

    @staticmethod
    def _subject(tag):
        return tag.find_all('a', class_="subject-link")[0].get_text()

    @staticmethod
    def _reflink(tag):
        s = str(tag.find_all('a')[0])
        bpos = s.find('/')
        epos = s.find('"', bpos)
        return "http://www.aconf.cn"+s[bpos:epos]

    @staticmethod
    def decode(tag):
        return {
            "name": DataTagDecoder._name(tag),
            "reflink": DataTagDecoder._reflink(tag),
            "position": DataTagDecoder._pos(tag),
            "bdate": DataTagDecoder._date(tag)[0],
            "edate": DataTagDecoder._date(tag)[1],
            "spnosor": DataTagDecoder._sponsor(tag),
            "subject": DataTagDecoder._subject(tag)}


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

    from DataHelper import MysqlCommiter

    commiter = MysqlCommiter()

    url = "http://www.aconf.cn/c.html?date_type=start_date&date_range=&start_date=1514736000&end_date=1514736000"
    html = requests.get(url).text

    decoder = DataTagDecoder()
    for tag in HtmlDecoder.dataTag(html):
        data = decoder.decode(tag)

        commiter.commit_confdata(
            data["name"],
            data["bdate"],
            data["edate"],
            data["reflink"],
            data["position"],
            data["spnosor"],
            data["subject"],

        )


def test_htmldecoder():
    url = "http://www.aconf.cn/c.html?date_type=start_date&date_range=&start_date=1524153600&end_date=1524153600"
    html = requests.get(url).text
    HtmlDecoder.dataHtmlUrl(html)


def main():
    test_tagdecorder()
    test_htmldecoder()


if __name__ == '__main__':
    main()
