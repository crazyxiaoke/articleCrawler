import os

'''
    读取properties配置文件工具
'''


class Property:
    def __init__(self, file_name):
        if os.path.exists(file_name):
            self.file_name = file_name
            self.properties = {}
            try:
                fopen = open(file_name, 'r')
                for line in fopen:
                    line = line.strip()
                    if line.find("=") > 0 and not line.startswith('#'):
                        strs = line.split("=")
                        self.properties[strs[0].strip()] = strs[1].strip()
            except Exception as e:
                raise e
            finally:
                fopen.close()
        else:
            print("file %s not found" % file_name)

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value


def parse(file_name):
    return Property(file_name)
