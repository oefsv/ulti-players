from importlib import import_module
import os
from .base import *

environment = os.getenv("ENVIRONMENT", "base")
l = locals()
d = import_module(f"ultimate_frisbee_management.settings.{environment}").__dict__

l.update(d)
