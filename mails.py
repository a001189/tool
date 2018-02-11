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
            if len(dir_list) > 0:
                try:
                    import filezip
                    for dirs in dir_list:
                        dir_name = os.path.basename(dirs.rstrip('/'))
                        dir_name_zip = dir_name + '.zip'
                        filezip.filezip(dirs, dir_name_zip)
                        msg.attach(self._attach_file(dir_name_zip))
                        os.remove(dir_name_zip)
                except Exception as e:
                    print(e, '文件压缩模块未加载,请下载同步下filezip.py，将跳过目录')

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


if __name__ == '__main__':
    a = Mail()
    s = a.send('201519832@qq.com', '你哈', '主题', 'content', 'a.ini,b.ini,log,' + r'D:\IDM')
    if s:
        print('发送成功')
