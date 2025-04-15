# coding=utf-8
from typing import Any

import os
import time
import calendar
from datetime import datetime

# from ka_uts_uts.utils.aoeqstmt import AoEqStmt
from ka_uts_arr.aoeqstmt import AoEqStmt
from ka_uts_uts.utils.pac import Pac
from ka_uts_uts.utils.pacmod import PacMod

from ka_uts_com.app import App
from ka_uts_com.cfg import Cfg
from ka_uts_com.exit import Exit

from ka_uts_log.log import Log

TyAny = Any
TyDateTime = datetime
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]

TnAny = None | Any
TnArr = None | TyArr
TnDic = None | TyDic
TnTimeStamp = None | TyTimeStamp
TnDateTime = None | TyDateTime
TnStr = None | str


class Com:
    """
    Communication Class
    """
    sw_init: bool = False
    dir_dat: TnStr = None
    tenant: TnStr = None
    log_type: TnStr = None
    cmd: TnStr = None
    d_com_pacmod: TyDic = {}
    d_app_pacmod: TyDic = {}
    path_bin = None
    path_log_cfg = None

    pid = None

    ts: TnTimeStamp
    ts_start: TnDateTime = None
    ts_end: TnDateTime = None
    ts_etime: TnDateTime = None
    d_timer: TyDic = {}

    Cfg: TnDic = None
    Log: Any = None
    App: Any = None
    Exit: Any = None

    @classmethod
    def init(cls, cls_app, kwargs: TyDic):
        """
        initialise static variables of Com class
        """
        if cls.sw_init:
            return
        cls.sw_init = True
        cls.dir_dat = kwargs.get('dir_dat', '/data')
        cls.tenant = kwargs.get('tenant')
        cls.log_type = kwargs.get('log_type', 'std')
        cls.cmd = kwargs.get('cmd')
        cls.d_com_pacmod = PacMod.sh_d_pacmod(cls)
        cls.d_app_pacmod = PacMod.sh_d_pacmod(cls_app)
        cls.ts = calendar.timegm(time.gmtime())
        cls.pid = os.getpid()

        cls.path_bin = cls.sh_path_bin()

        cls.Log = Log.sh(cls_app, **kwargs)
        cls.Cfg = Cfg.sh(cls, **kwargs)
        cls.App = App.sh(cls, **kwargs)
        cls.Exit = Exit.sh(**kwargs)

    @classmethod
    def sh_kwargs(cls, cls_app, d_parms, *args) -> TyDic:
        """
        show keyword arguments
        """
        _kwargs: TyDic = AoEqStmt.sh_d_eq(*args, d_parms=d_parms)
        cls.init(cls_app, _kwargs)
        _kwargs['com'] = cls
        return _kwargs

    @classmethod
    def sh_path_bin(cls) -> Any:
        """
        show path to bin directory in package
        """
        package = cls.d_app_pacmod['package']
        path = "bin"
        return Pac.sh_path_by_package(package, path)

    @classmethod
    def sh_path_data(cls) -> Any:
        """
        show path to data directory in package
        """
        package = cls.d_app_pacmod['package']
        path = "data"
        return Pac.sh_path_by_package(package, path)

    @classmethod
    def sh_path_cfg_yaml(cls) -> Any:
        """
        show path to configuration yaml-file in data directory of package
        """
        package = cls.d_app_pacmod['package']
        path = os.path.join('data', 'cfg.yml')
        return Pac.sh_path_by_package(package, path)
