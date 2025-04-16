from . import comparison
from . import matical
import warnings
from .. import colors
from toml import load
from pathlib import Path
from os import getenv

warnings.simplefilter('always', DeprecationWarning)
config = load(open(Path(getenv("appdata"),"xystudio", "pyplus", "config.toml"))) | load(open(Path(".xystudio", "pyplus", "config.toml").resolve()))
_show_warn = True

try:
    if config["library"]["showDeprecationWarning"] != "true":
        _show_warn = False
except KeyError:
    pass

if _show_warn:
    warnings.warn(
        colors.Fore.YELLOW + colors.Style.BRIGHT + "operators is deprecated since v1.2 and will be removed in v2.0. Please use operator (python built-in moudle)." + colors.Style.RESET_ALL,
        DeprecationWarning,
        stacklevel=2
    )