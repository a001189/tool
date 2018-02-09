#! /usr/local/bin python3.6
# @Time    : 2018/2/8 23:16
# @Author  : ysj
# @Site    : 
# @File    : excel.py
# @Software: PyCharm
import xlwt
import xlrd
import csv


class ExcelTools:
    """
    excel 处理工具 二进制xls ,csv格式
    """

    def __init__(self):
        pass

    def xls_read(self, files):
        """
        xls xlsx 格式读取，
        :param files:
        :return: 列表嵌套的生成器
        """
        wb = xlrd.open_workbook(files)
        sheet = wb.sheet_by_index(0)
        rows = sheet.get_rows()
        return ([cell.value for cell in row] for row in rows)

    def csv_read(self, files):
        """
        csv 读取，已知问题存在 文本格式，gbk，utf 等字节格式；采用try捕获；
        后期在完善其他未知错误或优化该问题
        :param files:
        :return: 列表嵌套的生成器
        """
        file = open(files, 'r', encoding='utf_8_sig')
        try:
            file.read(200)
        except UnicodeDecodeError:
            file = open(files, 'r')
        finally:
            file.seek(0, 0)
        rows = csv.reader(file)
        return (x for x in rows)

    def xls_write(self, data_list, files):
        """
        # 传入列表嵌套列表数据
        :param data_list:
        :param files:
        :return: 文件名 or 'error:errorinfo
        """
        try:
            wb = xlwt.Workbook(encoding='utf-8')
            sheet = wb.add_sheet('sheet1')
            style = xlwt.XFStyle()
            # 居中样式
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
            alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
            style.alignment = alignment
            for row, column in enumerate(data_list):
                for col, data in enumerate(column):
                    sheet.write(row, col, data, style)
            wb.save(files)
        except Exception as e:
            return 'error:' + str(e)
        return files

    def csv_write(self, data_list, files):
        """
        # 传入列表嵌套列表数据
        :param data_list:
        :param files:
        :return: 文件名 or 'error:errorinfo
        """
        csv_file = open(files, 'w', encoding='utf-8', newline='')
        writer = csv.writer(csv_file, dialect='excel', delimiter=',', quotechar='"')
        writer.writerows(data_list)
        return files


if __name__ == '__main__':
    exl = ExcelTools()
