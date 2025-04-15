from typing import Any
from collections.abc import Callable

import os
import time
import calendar
from datetime import datetime
import logging
import logging.config
from logging import Logger
import psutil

from ka_uts_uts.ioc.jinja2_ import Jinja2_
from ka_uts_uts.utils.pac import Pac
from ka_uts_uts.utils.pacmod import PacMod
# from ka_uts_uts.utils.aopath import AoPath
from ka_uts_arr.aopath import AoPath

TyAny = Any
TyCallable = Callable[..., Any]
TyDateTime = datetime
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyDir = str
TyPath = str
TyLogger = Logger
TyStr = str

TnAny = None | Any
TnArr = None | TyArr
TnBool = None | bool
TnDic = None | TyDic
TnTimeStamp = None | TyTimeStamp
TnDateTime = None | TyDateTime
TnStr = None | TyStr


class LogEq:
    """Logging Class
    """
    @staticmethod
    def sh(key: Any, value: Any) -> TyStr:
        return f"{key} = {value}"

    @classmethod
    def debug(cls, key: Any, value: Any) -> None:
        Log.debug(cls.sh(key, value), stacklevel=3)

    @classmethod
    def info(cls, key: Any, value: Any) -> None:
        Log.info(cls.sh(key, value), stacklevel=3)

    @classmethod
    def warning(cls, key: Any, value: Any) -> None:
        Log.warning(cls.sh(key, value), stacklevel=3)

    @classmethod
    def error(cls, key: Any, value: Any) -> None:
        Log.error(cls.sh(key, value), stacklevel=3)

    @classmethod
    def critical(cls, key: Any, value: Any) -> None:
        Log.critical(cls.sh(key, value), stacklevel=3)


class LogDic:

    @classmethod
    def debug(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.debug(key, value)

    @classmethod
    def info(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.info(key, value)

    @classmethod
    def warning(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.warning(key, value)

    @classmethod
    def error(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.error(key, value)

    @classmethod
    def critical(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.critical(key, value)


class Log:

    sw_init: bool = False
    log: TyLogger = logging.getLogger('dummy_logger')
    log_type: TyStr = 'std'
    pid = os.getpid()
    ts = calendar.timegm(time.gmtime())
    username: TyStr = psutil.Process().username()
    path_log_cfg: TyStr = ''
    d_pacmod: TyDic = {}
    d_app_pacmod: TyDic = {}

    @classmethod
    def debug(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.debug(*args, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.info(*args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.warning(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.error(*args, **kwargs)

    @classmethod
    def critical(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.critical(*args, **kwargs)

    @classmethod
    def sh_dir_run(cls, **kwargs) -> TyDir:
        """Show run_dir
        """
        dir_dat: str = kwargs.get('dir_dat', '/data')
        tenant: str = kwargs.get('tenant', '')
        package = cls.d_app_pacmod['package']
        path = os.path.join(dir_dat, tenant, 'RUN', package)
        cmd: TnStr = kwargs.get('cmd')
        if cls.log_type == "usr":
            path = os.path.join(path, cls.username)
        if cmd is not None:
            path = os.path.join(path, cmd)
        return path

    @classmethod
    def sh_d_dir_run_for_single_log(cls, **kwargs) -> TyDic:
        """Read log file path with jinja2
        """
        dir_run = cls.sh_dir_run(**kwargs)
        return {
                'dir_run_debs': f"{dir_run}/debs",
                'dir_run_infs': f"{dir_run}/logs",
        }

    @classmethod
    def sh_d_dir_run_for_multiple_logs(cls, **kwargs) -> TyDic:
        """Read log file path with jinja2
        """
        _dir_run = cls.sh_dir_run(**kwargs)
        return {
                'dir_run_debs': f"{_dir_run}/debs",
                'dir_run_infs': f"{_dir_run}/infs",
                'dir_run_wrns': f"{_dir_run}/wrns",
                'dir_run_errs': f"{_dir_run}/errs",
                'dir_run_crts': f"{_dir_run}/crts",
        }

    @classmethod
    def sh_d_log_cfg(cls, **kwargs) -> TyDic:
        """Read log file path with jinja2
        """
        if kwargs.get('sw_single_log_dir', True):
            d_dir_run = cls.sh_d_dir_run_for_single_log(**kwargs)
        else:
            d_dir_run = cls.sh_d_dir_run_for_multiple_logs(**kwargs)

        if kwargs.get('log_sw_mkdirs', True):
            AoPath.mkdirs(list(d_dir_run.values()), exist_ok=True)

        module = cls.d_app_pacmod['module']
        d_log_cfg: TyDic = Jinja2_.read(
                cls.path_log_cfg, cls.log,
                module=module, pid=cls.pid, ts=cls.ts, **d_dir_run)
        sw_debug: TyBool = kwargs.get('sw_debug', False)
        if sw_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logger_name = cls.log_type
        d_log_cfg['handlers'][f"{logger_name}_debug_console"]['level'] = level
        d_log_cfg['handlers'][f"{logger_name}_debug_file"]['level'] = level
        return d_log_cfg

    @classmethod
    def sh_path_log_cfg(cls) -> Any:
        """ show directory
        """
        _app_package = cls.d_app_pacmod['package']
        _package = cls.d_pacmod['package']
        _packages = [_app_package, _package]
        _path = os.path.join('cfg', f"log.{cls.log_type}.yml")
        return Pac.sh_path_by_packages(_packages, _path)

    @classmethod
    def init(cls, cls_app, **kwargs) -> None:
        """Set static variable log level in log configuration handlers
        """
        cls.sw_init = True

        cls.log_type = kwargs.get('log_type', 'std')
        _log_ts_type = kwargs.get('log_ts_type', 'ts')
        if _log_ts_type == 'ts':
            cls.ts = calendar.timegm(time.gmtime())
        else:
            cls.ts = calendar.timegm(time.gmtime())
        cls.d_pacmod = PacMod.sh_d_pacmod(cls)
        cls.d_app_pacmod = PacMod.sh_d_pacmod(cls_app)
        cls.path_log_cfg = cls.sh_path_log_cfg()
        _d_log_cfg = cls.sh_d_log_cfg(**kwargs)
        logging.config.dictConfig(_d_log_cfg)
        cls.log = logging.getLogger(cls.log_type)

    @classmethod
    def sh(cls, cls_app, **kwargs) -> Any:
        if cls.sw_init:
            return cls.log
        cls.init(cls_app, **kwargs)
        return cls
