import os
import sys
from datetime import datetime


def get_time_now() -> datetime:
    """Equal to dt.now() at the moment."""
    # TODO: add timezone
    return datetime.now()


def set_sys_path_cwd() -> None:
    """sys.path.append(os.getcwd())."""
    sys.path.append(os.getcwd())
