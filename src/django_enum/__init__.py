r"""
::

  ____  _                           _____                       
 |  _ \(_) __ _ _ __   __ _  ___   | ____|_ __  _   _ _ __ ___  
 | | | | |/ _` | '_ \ / _` |/ _ \  |  _| | '_ \| | | | '_ ` _ \ 
 | |_| | | (_| | | | | (_| | (_) | | |___| | | | |_| | | | | | |
 |____// |\__,_|_| |_|\__, |\___/  |_____|_| |_|\__,_|_| |_| |_|
     |__/             |___/                                     


Full and natural support for enumerations as Django model fields.
"""

from django_enum.fields import EnumField

__all__ = ["EnumField"]

VERSION = (2, 2, 2)

__title__ = "Django Enum"
__version__ = ".".join(str(i) for i in VERSION)
__author__ = "Brian Kohan"
__license__ = "MIT"
__copyright__ = "Copyright 2022-2025 Brian Kohan"
