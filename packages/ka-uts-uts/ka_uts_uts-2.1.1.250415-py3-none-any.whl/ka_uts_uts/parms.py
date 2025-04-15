from typing import Any
import warnings

warnings.filterwarnings("ignore")

TyDic = dict[Any, Any]
TyDoD = dict[Any, TyDic]
TyDoEq = dict[str, str | dict[str, str]]


class Parms:
    """
    Define valid Parameters with default values
    """
    d_eq: TyDoEq = {
        'cmd': 'str',
        'setup': {
            'cmd': 'str',

            'package': 'str',

            'src_dir_app': 'str',
            'src_dir_dat': 'str',
            'tgt_dir_app': 'str',
            'tgt_dir_dat': 'str',

            'log_sw_mkdirs': 'bool',
            'log_sw_single_dir': 'bool',
            'log_type': 'str',
            'log_ts_type': 'str',
            'tenant': 'str',
            'sw_debug': 'bool',
        },
    }
