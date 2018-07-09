class Article(object):

    def __init__(self, title='', url=''):
        self.__id = 0
        self.__title = title  # 标题
        self.__url = url  # 原始链接
        self.__author = ''  # 作者
        self.__content = ''  # 内容
        self.__contentHead = ''  # 简要
        self.__createTime = ''  # 创建时间
        self.__thumbnailUrl = ''  # 缩略图
        self.__type = ''  # 类型

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def contentHead(self):
        return self.__contentHead

    @contentHead.setter
    def contentHead(self, contentHead):
        self.__contentHead = contentHead

    @property
    def createTime(self):
        return self.__createTime

    @createTime.setter
    def createTime(self, createTime):
        self.__createTime = createTime

    @property
    def thumbnailUrl(self):
        return self.__thumbnailUrl

    @thumbnailUrl.setter
    def thumbnailUrl(self, thumbnailUrl):
        self.__thumbnailUrl = thumbnailUrl

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type
