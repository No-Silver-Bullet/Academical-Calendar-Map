#! coding:utf8

import MySQLdb
import datetime
from config import config


class MysqlCommiter(object):

    def __init__(self):
        """
            ctor
        """
        self.sqls = []
        self.conn = MySQLdb.connect(config['mysql-default']['host'], config['mysql-default']['username'],
                                    config['mysql-default']['passwd'], config['mysql-default']['dbname'],
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def __del__(self):
        """
            dtor
        """
        for sql in self.sqls:
            try:
                self.cur.execute(sql)
            except Exception as err:
                pass

        self.conn.commit()

    def _commit(self, sql):
        """
            add sql to cache, or commit them all
        """
        if len(self.sqls) > config['mysql-default']['commit-frequency']:

            for sql in self.sqls:
                try:
                    # print sql
                    self.cur.execute(sql)
                except Exception as err:
                    print err
                    pass

            self.conn.commit()

            print "[PYTHON-a324] 已提交%s条sql" % len(self.sqls)

            self.sqls = []
        else:
            self.sqls.append(sql)

    def commit_confdata(self, name, btime, etime, refurl, locate, sponsor, subject):

        s = 'insert into conference (name,time_begin,time_end,reference_url,locate,sponsor,subject)\
            values("%s","%s","%s","%s","%s","%s","%s")' % (
            name, btime, etime, refurl, locate, sponsor, subject
        )

        print s
        self._commit(s)
