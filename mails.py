#! /usr/local/bin python3.6
"""
@Time    : 2018/2/11 1:24
@Author  : ysj
@Site    : 
@File    : email.py
@Software: PyCharm
"""
import smtplib
import os
import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Mail:
    """
    邮件发送类
    """
    def __init__(self, server='smtp.163.com', port=25, user='18516157608@163.com', password='123123qwe', ssl=False):
        self._server = server
        self._port = port
        self._user = user
        self._password = password
        self._ssl = ssl

    def server(self):
        server = smtplib.SMTP()
        server.connect(self._server, self._port)  # 连接服务器
        server.login(self._user, self._password)  # 登录操作
        return server

    def send(self, to_list, from_man, subject, content, attach_file=None, subtype='plain'):
        """

        :param to_list:  收件人以半角逗号分隔 必填
        :param from_man:  发件人别名，必填
        :param subject: 主题
        :param content: 正文
        :param subtype: 编码类型，plain -->文本 html -->网页格式
        :param attach_file: 附件，多个附件以，；分割
        :return: 发送成功，则为真
        """
        msg = MIMEMultipart()
        msg['Subject'] = subject  # 标题
        fr = from_man + "<" + self._user + ">"
        print(fr, type(fr))
        msg['From'] = fr  # 发件人
        msg['To'] = to_list  # 收件人，必须是一个字符串
        # 邮件正文内容
        msg.attach(MIMEText(content, subtype, 'utf-8'))
        if attach_file:
            path_list = self.file_to_list(attach_file)
            print(path_list)
            dir_list = [x for x in path_list if os.path.isdir(x)]
            file_list = [x for x in path_list if not os.path.isdir(x)]
            for file in file_list:
                msg.attach(self._attach_file(file))
            for dirs in dir_list:
                dir_name = os.path.basename(dirs.rstrip('/'))
                dir_name_zip = dir_name + '.zip'
                self.filezip(dirs, dir_name_zip)
                msg.attach(self._attach_file(dir_name_zip))
                os.remove(dir_name_zip)

        # 发送
        try:
            server = smtplib.SMTP()
            server.connect(self._server, self._port)  # 连接服务器
            server.login(self._user, self._password)  # 登录操作
            server.sendmail(fr, to_list.split(','), msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def _attach_file(path):
        if not os.path.isfile(path):
            raise FileNotFoundError('{0} file does not exist'.format(path))
        filename = os.path.basename(path)
        # 构造附件1，传送当前目录下的 test.txt 文件
        att = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
        return att

    @staticmethod
    def file_to_list(path):
        """
        根据路径中，；分割多个路径；文件夹则压缩文件夹
        :param path:
        :return:
        """
        if path:
            path_list = path.replace(';', ',').split(',')
            return [x.strip() for x in path_list]

    def filezip(self, path: str='输入文件', file_path: str='压缩结果文件'):
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
                        for file in self.dir_list(ph):
                            zpfile[file] = file.replace(parent_path, '')
        for path, filename in zpfile.items():
            zp.write(path, filename)
            print('add %s' % path)
        zp.close()
        return file_path

    @staticmethod
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
    a = Mail()
    s = a.send('201519832@qq.com', '你哈', '主题', '不错呀。小伙子', 'a.ini,b.ini,log,' + r'D:\IDM')
    if s:
        print('发送成功')
