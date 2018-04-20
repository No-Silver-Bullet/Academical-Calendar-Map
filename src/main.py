#! coding:utf8

import Decoder
import DataHelper
import Spider
import datetime
import time
import random


def datestr_to_time(s):
    date = datetime.datetime.strptime(s, "%Y-%m-%d")
    rv = int(time.mktime(date.timetuple()))
    return rv


def time_to_datestr(t):
    return datetime.datetime.fromtimestamp(t)


def get_data(date):
    url = "http://www.aconf.cn/c.html?date_type=start_date&date_range=&start_date=%s&end_date=%s" % (
        date, date)
    data = []

    html = Spider.Spider.get_url(url)
    urls = Decoder.HtmlDecoder.dataHtmlUrl(html.text)

    for u in urls:
        html = Spider.Spider.get_url(u)
        datatags = Decoder.HtmlDecoder.dataTag(html.text)
        for tag in datatags:
            d = Decoder.DataTagDecoder.decode(tag)
            data.append(d)

    # for d in data:
    #     for key in d.keys():
    #         print key, ":", d[key], " "
    #     print ""

    return data


def sleep():
    """
        每1-3分钟sleep一下
    """
    duration = random.randint(20, 60)*3
    time.sleep(duration)


def work():
    bdate = datestr_to_time("2018-04-01")
    edate = datestr_to_time("2018-12-31")

    commiter = DataHelper.MysqlCommiter()

    while bdate < +edate:

        datas = get_data(bdate)
        print "[PYTHON-asd1],%s %s条数据" % (time_to_datestr(bdate),
                                          len(datas))

        for data in datas:
            commiter.commit_confdata(
                data["name"],
                data["bdate"],
                data["edate"],
                data["reflink"],
                data["position"],
                data["spnosor"],
                data["subject"],

            )

        bdate += 3600

        sleep()


def main():
    work()


if __name__ == '__main__':
    main()
