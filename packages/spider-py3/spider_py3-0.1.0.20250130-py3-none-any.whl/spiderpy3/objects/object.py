import os
import inspect
from abc import ABCMeta
from typing import Any
from typing_extensions import Self

from spiderpy3.utils.logger import logger


class ObjectMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        module = inspect.getmodule(cls)
        if module and hasattr(module, "__file__"):
            file_path = os.path.abspath(module.__file__)
            cls.dir_path = os.path.dirname(file_path)
        else:
            cls.dir_path = None
        return cls


class Object(object, metaclass=ObjectMeta):
    logger = logger
    dir_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_instance(cls, *args: Any, **kwargs: Any) -> Self:
        return cls(*args, **kwargs)
