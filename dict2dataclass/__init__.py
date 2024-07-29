from .from_dict import FromDict
from .dict_field import dict_field

__all__ = ["FromDict", "dict_field"]

import logging

# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("dataclass_wizard").addHandler(logging.NullHandler())
