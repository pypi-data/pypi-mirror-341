"""
This module provides task scheduling classes for the management of OmniTracker
SRR (NHRR) processing for Department UMH.
    SRR: Sustainability Risk Rating
    NHRR: Nachhaltigkeits Risiko Rating
"""
import os
# import os.PathLike
import shutil

from ka_uts_uts.utils.pac import Pac

from typing import Any

TyPathLike = os.PathLike
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
# TyAoA = list[TyArr]
# TyAoD = list[TyDic]
# TyDoAoA = dict[Any, TyAoA]
# TyDoAoD = dict[Any, TyAoD]

# TyPath = str
# TyPath = str | TyPathLike[str] | bytes | TyPathLike[bytes]

TnAny = None | Any
# TnAoD = None | TyAoD
TnDic = None | TyDic
# TnPath = None | TyPath


class Setup:
    """
    Setup function class
    """
    @classmethod
    def setup(cls, kwargs: TyDic) -> None:
        _package: str = kwargs.get('package', '')
        _src_dir_app: Any = kwargs.get('src_dir_app', '')
        _src_dir_dat: Any = kwargs.get('src_dir_dat', '')
        _tgt_dir_app: Any = kwargs.get('tgt_dir_app', '')
        _tgt_dir_dat: Any = kwargs.get('tgt_dir_dat', '')
        _pac_src_dir_app: Any = Pac.sh_path_by_package(_package, _src_dir_app)
        _pac_src_dir_dat: Any = Pac.sh_path_by_package(_package, _src_dir_dat)
        print(f" setup _pac_src_dir_app = {_pac_src_dir_app}")
        print(f" setup _pac_src_dir_dat = {_pac_src_dir_dat}")
        cls.copytree(_pac_src_dir_app, _tgt_dir_app)
        cls.copytree(_pac_src_dir_dat, _tgt_dir_dat)

    @staticmethod
    def copytree(src: Any, tgt: Any) -> None:
        if not src:
            return
        if not os.path.exists(tgt):
            os.makedirs(tgt)
        shutil.copytree(src, tgt, dirs_exist_ok=True)
