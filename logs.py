#! /usr/local/bin python3.6
"""
@Time    : 2018/2/10 17:55
@Author  : ysj
@Site    : 
@File    : logs.py.py
@Software: PyCharm
"""
import os
import inspect
import logging


class Loginfo:
    """
    日志记录
    格式 日期，标识flag，level，文件名 行号 输出信息
    """
    def __init__(self, log_file='log.log', flag='tmp'):
        self.flag = flag
        self.logflie = log_file
        self.fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d %(message)s'
        # 判断日志文件path,不存在则创建；分相对、绝地路径
        if self.logflie:
            log_dir = os.path.dirname(self.logflie)
            if log_dir:  # 不包含路径时，不检查父目录存在与否
                os.path.exists(log_dir) or os.makedirs(log_dir)
        else:
            raise InterruptedError('logfile path is required')

        log_name = os.path.basename(self.logflie)
        if not log_name and os.path.isdir(self.logflie):
            raise InterruptedError('the logfile should not be a dir ')
        setattr(self, 'DEBUG', logging.DEBUG)

    def write_log(self, message, level='debug', to_file=True, to_terminal=False):
        logger = logging.getLogger(self.flag)
        log_level = getattr(logging, level.upper(), 0)
        logger.setLevel(log_level)
        # 定义handler的输出格式
        formatter = logging.Formatter(self.fmt)
        # 创建一个handler用于写入日志文件
        if to_file:
            fh = logging.FileHandler(self.logflie)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            getattr(logger, level, logger.debug)(message)
            fh.flush()
            logger.removeHandler(fh)
        # 创建一个handler用于输出到终端
        if to_terminal:
            th = logging.StreamHandler()
            th.setFormatter(formatter)
            logger.addHandler(th)
            getattr(logger, level, logger.debug)(message)
            th.flush()
            logger.removeHandler(th)

    def debug(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)

    def info(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)

    def warning(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)

    def error(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)

    def info(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)

    def critical(self, message, to_file=True, to_terminal=False):
        level = inspect.stack()[0][3]
        return self.write_log(message, level=level, to_file=to_file, to_terminal=to_terminal)


if __name__ == "__main__":
    lg = Loginfo('log/log.log')
    lg.info('dsadaads')
    lg.error('shabshab')
    lg.debug('debug')
    lg.critical('dasdasdssaddddddd')
    lg.warning('warning')

