import os


BASE_DIR = os.path.dirname(__file__)
__config__ = os.path.abspath(os.path.join(BASE_DIR, "../config.cfg"))

__template__ = os.path.abspath(os.path.join(BASE_DIR, "templates"))
__static__ = os.path.abspath(os.path.join(BASE_DIR, "static"))
__upload__ = os.path.abspath(os.path.join(__static__, "uploads"))
