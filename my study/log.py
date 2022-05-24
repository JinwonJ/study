from datetime import datetime
from typing import Callable, Union
from termcolor import colored


class Loggable:

    @classmethod
    def log_(cls, *args, **kwargs):
        to_stringified = []
        for arg in args:
            to_stringified.append(str(arg))

        line = ' '.join([
            '[' + datetime.now().isoformat(timespec='seconds') + ']',
            '[' + cls.__name__ + ']',
            *to_stringified
        ])

        line_color = kwargs.get('color')
        if line_color:
            line = colored(line, line_color)

        print(line)

    @classmethod
    def debug_(cls, *args):
        cls.log_(*args, color='yellow')

    @classmethod
    def warn_(cls, *args):
        cls.log_(*args, color='magenta')

    @classmethod
    def error_(cls, *args):
        cls.log_(*args, color='red')

    def _log(self, *args, **kwargs):
        self.__class__.log_(*args, **kwargs)

    def _warn(self, *args):
        self.__class__.warn_(*args)

    def _debug(self, *args):
        self.__class__.debug_(*args)

    def _register(self, method: str, name_or_callback: Union[str, Callable], callback: Callable = None):
        if callback:
            self.__class__.debug_(
                'Register',
                colored(method),
                colored(name_or_callback, 'cyan'),
                colored(callback.__name__, 'magenta')
            )
        elif isinstance(name_or_callback, str):
            self.__class__.debug_(
                'Register',
                colored(method),
                colored(name_or_callback, 'cyan'),
            )
        else:
            self.__class__.debug_(
                'Register',
                colored(method),
                colored(name_or_callback.__name__, 'magenta')
            )
