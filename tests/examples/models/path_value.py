from django.db import models
from enum import Enum
from django_enum import EnumField
from pathlib import PurePosixPath


class PathValueExample(models.Model):

    class PathEnum(Enum):

        USR = PurePosixPath('/usr')
        USR_LOCAL = PurePosixPath('/usr/local')
        USR_LOCAL_BIN = PurePosixPath('/usr/local/bin')

    path = EnumField(PathEnum, primitive=str)
