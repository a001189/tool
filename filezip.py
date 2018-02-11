#! /usr/local/bin python3.6
"""
@Time    : 2018/2/11 16:45
@Author  : ysj
@Site    : 
@File    : filezip.py
@Software: PyCharm
"""
import os
import zipfile


def filezip(path: str='输入文件', file_path: str='压缩结果文件'):
    """
    压缩目录，或文件
    :param path: 多个文件，目录的路径，以";"或","分割
    :param file_path: 压缩结果文件
    :return:
    """
    if not (file_path and file_path.endswith('zip')):
        raise InterruptedError('请输入压缩结果文件:*.zip')
    zp = zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED)
    zpfile = dict()
    if path:
        path_list = [x.strip() for x in path.replace(";", ",").split(",")]
        for ph in path_list:
            if not os.path.exists(ph):
                print('%s不存在，跳过该文件' % ph)
            else:
                if os.path.isfile(ph):
                    zpfile[ph] = os.path.basename(ph)
                else:
                    # 变目录的绝对路径为相对路径
                    parent_path = os.path.split(ph.rstrip('/'))[0]
                    for file in dir_list(ph):
                        zpfile[file] = file.replace(parent_path, '')
    for path, filename in zpfile.items():
        zp.write(path, filename)
        print('add %s' % path)
    zp.close()
    print(zpfile)

    import conf
    conf.DictToConfig(zpfile, 'zp.yaml')()

    return file_path


def dir_list(path_dir):
    file_list = list()

    def listdir(path):
        """
        遍历目录
        :param path:
        :return:
        """
        for ph in os.walk(path):
            # 文件
            for file in ph[2]:
                file_list.append(os.path.join(ph[0], file).replace('\\', '/'))
            for dirs in ph[1]:
                listdir(os.path.join(ph[0], dirs).replace('\\', '/'))
        return file_list
    return listdir(path_dir)


if __name__ == '__main__':
    print(dir_list('/Users/y/Desktop/tool'))
    print(filezip('a.ini,/Users/y/Desktop/tool/a,/Users/y/Downloads/Documents', 'result.zip'))
