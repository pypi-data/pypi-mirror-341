from os.path import dirname, basename, isfile, join
import glob
import logging
from pathlib import Path


modules = glob.glob(join(dirname(__file__), "*.py")) + glob.glob(
    join(dirname(__file__), "*.so")
)
__all__ = [
    Path(f).name.split(".")[0]
    for f in modules
    if isfile(f) and not f.endswith("__init__.py") and not f.endswith(
        "setup.py"
    )
]

base_pkg = basename(__path__[0])
for module_name in __all__:
    i = __import__(base_pkg + "." + module_name)

logging.getLogger(__name__).addHandler(logging.NullHandler())
