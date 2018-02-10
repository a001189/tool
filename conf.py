#! /usr/local/bin python3.6
"""
@Time    : 2018/2/10 1:08
@Author  : ysj
@Site    : 
@File    : conf.py
@Software: PyCharm
"""
import os
import configparser
import json
import yaml


class ConfigToDict:
    """
    解析配置文件 conf，ini ；yaml；json；
    备选 hocon xml
    :return:
    """
    def __init__(self, path=None, category=None):
        self.path = path
        self.category = category
        if not (path and os.path.exists(path)):
            raise InterruptedError('未指定配置文件路径或配置文件不存在')

    def conf_explain(self):
        """
        返回有序自字典
        :return:
        """
        configs = configparser.ConfigParser()
        configs.read(self.path)
        return configs._sections

    def json_explain(self):
        """
        返回字典
        :return:
        """
        json_data = json.loads(open(self.path).read())
        return json_data

    def yaml_explain(self):
        """
        返回yaml字典
        :return:
        """
        return yaml.load(open(self.path))


class DictToConfig:
    """
    生成配置文件 conf，ini ；yaml；json；
    备选 hocon xml
    :return:
    """
    def __init__(self, path=None, category=None):
        self.path = path
        self.category = category
        if not path:
            raise InterruptedError('未指定配置文件路径')

    def to_conf(self, data):
        """
        输入数据必须嵌套字典
        :param data:
        :return: 返回 self.path 配置文件
        """
        config = configparser.ConfigParser()
        if isinstance(data, dict) and False not in [isinstance(value, dict) for value in data.values()]:
            print([[key, key1, value1]for key, value in data.items() for key1, value1 in value.items()])
            for key, value in data.items():
                config.add_section(str(key))
                for key1, value1 in value.items():
                    config.set(str(key), str(key1), str(value1))
            with open(self.path, 'w') as f:
                config.write(f)
            return self.path
        else:
            raise TypeError('输入数据必须为嵌套字典')

    def to_ini(self, data):
        """
        ini 与 conf 相同 指向同一函数
        :param data:
        :return:
        """
        return self.to_conf(data)

    def to_json(self, data):
        """
        传入字典生成json文件
        :param data:
        :return:
        """
        if isinstance(data, dict):
            with open(self.path, 'w') as f:
                json.dump(data, f)
            return self.path
        else:
            raise TypeError('输入数据必须为字典')

    def to_yaml(self, data):
        """
               传入字典生成yaml文件 ;格式不标准，嵌套的字典会显示成字典形式
               :param data:
               :return:
               """
        if isinstance(data, dict):
            with open(self.path, 'w') as f:
                yaml.dump(data, f)
            return self.path
        else:
            raise TypeError('输入数据必须为字典')


if __name__ == '__main__':
    conf = ConfigToDict('a.ini')
    print(json.dumps(conf.conf_explain()))
    js = ConfigToDict('a.json')
    print(js.json_explain())
    ym = ConfigToDict('a.yaml')
    print(ym.yaml_explain())
    ini = DictToConfig('b.ini')
    print(ini.to_conf({1: {1: 2, 2: {2: 3}}, }))
    js2 = DictToConfig('b.json')
    print(js2.to_json({1: {1: 2, 2: {2: 3}}, }))
    ym2 = DictToConfig('b.yaml')
    print((ym2.to_yaml(ym.yaml_explain())))