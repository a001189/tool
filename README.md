"# tool" 
#### python
 * 版本 python3
 * 需包含以下模块 configparser json yaml
#### excel.py
 1. csv xls xlsx格式excel的读操作， 返回 为嵌套列表的生成器对象
 2. csv xls xlsx格式excel的写操作， 返回 文件名。 传入参数为列表的迭代对象

#### conf.py
- 针对 conf ini yaml json 几种格式配置文件的读写
  1. 传入配置文件，根据后缀自动识别类型，或指定类型（优先级高于自动识别） 返回字典对象
  2. 将字典类型写入配置文件，根据后缀自动识别类型，或指定类型（优先级高于自动识别）返回文件路径， 输入为字典对象，（ini，conf 需要为嵌套字典）
- 使用方法
  1. 实例化类，并调用该类 ConfigToDict('a.json')() 读配置，返回字典
  2. 实例化类，并调用该类 DictToConfig({1: {1: 2, 2: {2: 3}}, }, 'c.yaml')() 写配置，返回文件路径
#### logs.py
- 日志记录对象，使用logging基础包，进行日志的记录和打印
- 定义了5种级别的日志，与logging包的对应
- 使用方法
  1. 实例化类，指定输出日志文件
  2. 使用 实例的 info，debug，warning等方法写入对应级别的日志
