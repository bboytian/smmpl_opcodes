from .file_check import main as file_check
from .file_delete import main as file_delete

from .file_man.__main__ import main as file_man
from .file_man.mpl2solaris_datasync import main as mpl2solaris_datasync

from .sigmampl_boot.__main__ import main as sigmampl_boot
from .sigmampl_boot.scan_init import main as scan_init

from .sigmampl_boot.sigmampl_startkill import sigmampl_kill as _sigmampl_kill
from .sigmampl_boot.prepostmea_fileman import postmea_fileman as _postmea_fileman

from .file_man.mpl2solaris_datasync import main as _mpl2solaris_datasync
from .file_man.mpl_organiser import main as _mpl_organiser

from .webswitch_logger import main as webswitch_logger
