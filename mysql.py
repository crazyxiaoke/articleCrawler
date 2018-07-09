import pymysql
import traceback
import property
from Article import Article

"""
    操作数据库
"""


class Mysql(object):

    def __init__(self):
        try:
            properies = property.parse('config/db.properties')
        except Exception as e:
            print('读取配置失败:', e)
        try:
            print('开始链接')
            self.conn = pymysql.connect(
                host=properies.get('host'),
                port=properies.get('port'),
                user=properies.get('user'),
                passwd=properies.get('passwd'),
                db=properies.get('database'),
                charset=properies.get('charset')
            )
        except Exception as e:
            print("数据库连接失败:", e)
        else:
            print('数据库连接成功')
            self.cur = self.conn.cursor()

    def query(self, title):
        sql = u'select count(*) from web_information where title="{0}"'.format(title)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        return res[0]

    def queryList(self):
        sql = u'select id,title,content,contentHead from web_information'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        articles = []
        for item in res:
            article = Article()
            article.id = item[0]
            article.title = item[1]
            article.content = item[2]
            article.contentHead = item[3]
            articles.append(article)
        return articles

    def insert(self, article: Article):
        if not article:
            raise AttributeError("AttributeError:'article' object is null")
        if self.query(article.title) > 0:
            raise RuntimeError("该条记录数据库已存在")
        sql = u'insert into web_information(title,author,content,contentHead,thumbnailUrl,type) ' \
              'values("{0}","{1}","{2}","{3}","{4}","{5}","{6}")' \
            .format(article.title, article.author, article.content, article.contentHead, article.thumbnailUrl,
                    article.type)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("数据插入失败:", e)
            print(traceback.format_exc())
            self.conn.rollback()

    def insert_array(self, articles: [Article]):
        if articles:
            for article in articles:
                if self.query(article.title) > 0:
                    continue
                print(type(article.contentHead))
                if not article.content:
                    print("========空=========")
                content = article.content
                contentHead = article.contentHead
                sql = 'insert into web_information(title,author,content,contentHead,thumbnailUrl,type) ' \
                      'values(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\")' \
                    .format(article.title, article.author, pymysql.escape_string(article.content),
                            pymysql.escape_string(article.contentHead)
                            , article.thumbnailUrl,
                            article.type)
                print(sql)
                self.cur.execute(sql)
            try:
                self.conn.commit()
            except Exception as e:
                print("数据插入失败:", e)
                print(traceback.format_exc())
                self.conn.rollback()

    def update(self, articles: Article):
        print("==========数据更新开始============")
        if articles:
            for article in articles:
                sql = 'update web_information set content=\"{0}\",contentHead="{1}" where id={2}'.format(
                    pymysql.escape_string(article.content), pymysql.escape_string(article.contentHead), article.id)
                print(sql)
                self.cur.execute(sql)
            try:
                self.conn.commit()
            except Exception as e:
                print("数据更新失败：", e)
                self.conn.rollback()
        print("==========数据更新完成============")

    def close(self):
        self.conn.close()
        self.cur.close()
