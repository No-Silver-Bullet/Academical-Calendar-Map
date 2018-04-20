#! coding:utf8

import requests


class Spider(object):
    @staticmethod
    def get_url(url):
        return requests.get(url)
