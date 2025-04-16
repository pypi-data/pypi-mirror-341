#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# datetime:2025/04/02
import os
import re
import json
import socket
import inspect
import logging
import datetime
import platform
import threading
from logging.handlers import TimedRotatingFileHandler
from filelock import FileLock

"""
pip install filelock
"""


class SafeTimedRotatingHandler(TimedRotatingFileHandler):
    """进程安全的日志轮转处理器"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock_file = f"{self.baseFilename}.lock"

    def doRollover(self):
        with FileLock(self.lock_file):  # 进程级文件锁
            if not os.path.exists(self.baseFilename + ".1"):
                super().doRollover()


class DateEncoder(json.JSONEncoder):
    """json序列化datetime类型"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


class LogMiddleware(object):
    _instance_lock = threading.Lock()
    log_dict = {}

    def __init__(self, log_dir_path,
                 app_name="Test_app",
                 hostname=socket.gethostname(),
                 log_level="DEBUG",
                 log_format_model="elk",
                 log_when="H",
                 log_interval=1,
                 log_backup_count=30 * 24):
        """
        :param log_dir_path: 日志存放基目录
        :param app_name: 应用标识
        :param hostname: 主机名
        :param log_level: 日志级别
        :param log_format_model: 日志格式模板,日志记录的格式,可以选设置好的default或elk，也可以自定义
        :param log_when: 轮转周期(H/M/S),日志分割的模式：H 小时，M 分钟，S 秒
        :param log_interval: 轮转间隔,日志分割的维度，仅支持天D、小时H，分钟M，秒S
        :param log_backup_count: 保留日志数量,，默认按小时分割，保留30天的日志
        """
        self.app_name = app_name
        self.hostname = hostname
        self.log_level = log_level
        self.log_dir_path = log_dir_path
        self.log_format_model = log_format_model
        self.log_when = log_when.upper()
        self.log_interval = log_interval
        self.log_backup_count = log_backup_count
        self.logger = self.__class__.__name__

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(LogMiddleware, "_instance"):
            with LogMiddleware._instance_lock:
                if not hasattr(LogMiddleware, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def get_logger(self):
        """获取进程安全的日志器"""
        p_id = str(os.getpid())
        logger_ = self.log_dict.get("p" + p_id)
        if not logger_:
            # 日志格式配置
            log_format_dict = {
                "default": "[%(levelname)s]:[%(asctime)s]:(thread_id:%(thread)d):[%(filename)s:%(lineno)d]-%(message)s",
                "elk": "%(message)s"
            }
            def_format = logging.Formatter(
                log_format_dict[self.log_format_model]
                if self.log_format_model in log_format_dict.keys()
                else self.log_format_model)

            # 日志目录处理
            if platform.system() == 'Windows':
                log_path_prefix = os.path.join(self.log_dir_path, "log")
            else:
                log_path_prefix = os.path.join("/app/log/", os.path.basename(self.log_dir_path))
            if not os.path.exists(log_path_prefix):
                os.makedirs(log_path_prefix)

            # 创建各级别日志处理器
            debug_handler = self._create_handler(
                f"{log_path_prefix}/{self.app_name}_code-info-{self.hostname}.log",
                logging.DEBUG,
                def_format,
                lambda r: r.levelno < logging.INFO
            )

            info_handler = self._create_handler(
                f"{log_path_prefix}/{self.app_name}_info-info-{self.hostname}.log",
                logging.INFO,
                def_format,
                lambda r: r.levelno < logging.WARNING
            )

            warn_handler = self._create_handler(
                f"{log_path_prefix}/{self.app_name}_code-warn-{self.hostname}.log",
                logging.WARNING,
                def_format,
                lambda r: r.levelno < logging.ERROR
            )

            error_handler = self._create_handler(
                f"{log_path_prefix}/{self.app_name}_code-error-{self.hostname}.log",
                logging.ERROR,
                def_format,
                None
            )

            # 创建日志器
            logger_ = logging.getLogger(f"{self.app_name}_{p_id}")
            logger_.setLevel(self.log_level)
            for handler in [debug_handler, info_handler, warn_handler, error_handler]:
                logger_.addHandler(handler)

            self.log_dict["p" + p_id] = logger_
        return logger_

    def _create_handler(self, path, level, log_msg_format, filter_func=None):
        """创建安全的日志处理器"""
        handler = SafeTimedRotatingHandler(
            # 文件地址包含文件名
            path,
            # 分割的维度
            when=self.log_when,
            # 如按秒分割，间隔5秒，从执行程序开始计时，如第1开始，分割就是第6
            interval=self.log_interval,
            # 保留日志个数，默认30天的日志
            backupCount=self.log_backup_count,
            encoding='utf-8'
        )
        # 设置分割日志后文件名的后缀格式
        handler.suffix = self._get_suffix_format()
        # 设置不符合日志文件名规则的删除日志文件
        handler.extMatch = re.compile(self._get_ext_match())
        # 设置日志级别
        handler.setLevel(level)
        # 设置日志格式
        handler.setFormatter(log_msg_format)
        if filter_func:
            handler.addFilter(filter_func)
        return handler

    def _get_suffix_format(self):
        """获取日志文件后缀格式"""
        return {
            "D": "%Y%m%d.log",
            "H": "%Y%m%dT%H.log",
            "M": "%Y-%m-%d_%H-%M.log",
            "S": "%Y-%m-%d_%H-%M-%S.log"
        }.get(self.log_when, "%Y%m%d.log")

    def _get_ext_match(self):
        """获取日志文件匹配正则"""
        return {
            "D": r"^\d{4}\d{2}\d{2}.log$",
            "H": r"^\d{4}\d{2}\d{2}T\d{2}.log$",
            "M": r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$",
            "S": r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.log$"
        }.get(self.log_when, r"^\d{8}.log$")

    def base_model(self, log_type, levelno, level, message, path_name, lineno, func_name, extra=None, app_name=None):
        """构建基础日志模型"""
        data = {
            "app_name": app_name or f"{self.app_name}_code",
            "logger": self.logger,
            "host_name": self.hostname,
            "log_type": log_type,
            "level_no": levelno,
            "log_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "level": level,
            "thread": str(threading.currentThread().ident),
            "code_message": message,
            "pathName": path_name,
            "lineNo": lineno,
            "funcName": func_name,
        }
        if extra:
            data.update(extra)
        return json.dumps(data, ensure_ascii=False, cls=DateEncoder)

    def debug(self, msg, log_type="desc"):
        """DEBUG级别日志"""
        if logging.DEBUG >= logging.getLevelName(self.log_level):
            path_name, lineno, func_name = self._get_caller_info()
            self.get_logger().debug(self.base_model(
                log_type=log_type,
                levelno=logging.DEBUG,
                level="INFO",
                message=msg,
                path_name=path_name,
                lineno=lineno,
                func_name=func_name
            ))

    def info(self, msg, log_type="desc"):
        """INFO级别日志"""
        if logging.INFO >= logging.getLevelName(self.log_level):
            path_name, lineno, func_name = self._get_caller_info()
            self.get_logger().info(self.base_model(
                log_type=log_type,
                levelno=logging.INFO,
                level="INFO",
                message=msg,
                path_name=path_name,
                lineno=lineno,
                func_name=func_name
            ))

    def warning(self, msg, log_type="desc"):
        """WARNING级别日志"""
        if logging.WARNING >= logging.getLevelName(self.log_level):
            path_name, lineno, func_name = self._get_caller_info()
            self.get_logger().warning(self.base_model(
                log_type=log_type,
                levelno=logging.WARNING,
                level="WARNING",
                message=msg,
                path_name=path_name,
                lineno=lineno,
                func_name=func_name
            ))

    def error(self, msg, log_type="desc"):
        """ERROR级别日志"""
        if logging.ERROR >= logging.getLevelName(self.log_level):
            path_name, lineno, func_name = self._get_caller_info()
            self.get_logger().error(self.base_model(
                log_type=log_type,
                levelno=logging.ERROR,
                level="ERROR",
                message=msg,
                path_name=path_name,
                lineno=lineno,
                func_name=func_name
            ))

    def external(self, msg, extra, log_type="monitor"):
        """外部监控日志"""
        path_name, lineno, func_name = self._get_caller_info()
        self.get_logger().info(self.base_model(
            log_type=log_type,
            levelno=60,  # EXTERNAL级别
            level="INFO",
            message=msg,
            path_name=path_name,
            lineno=lineno,
            func_name=func_name,
            extra=extra,
            app_name=f"{self.app_name}_info"
        ))

    def internal(self, msg, extra, log_type="monitor"):
        """内部监控日志"""
        path_name, lineno, func_name = self._get_caller_info()
        self.get_logger().info(self.base_model(
            log_type=log_type,
            levelno=60,  # INTERNAL级别
            level="INFO",
            message=msg,
            path_name=path_name,
            lineno=lineno,
            func_name=func_name,
            extra=extra,
            app_name=f"{self.app_name}_info"
        ))

    def _get_caller_info(self):
        """获取调用者信息"""
        frame = inspect.stack()[2]  # 跳过两层调用栈
        return frame.filename, frame.lineno, frame.function