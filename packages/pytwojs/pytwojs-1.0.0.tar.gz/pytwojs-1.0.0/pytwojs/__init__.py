__package__ = 'pytwojs'

from typing import Union as _Union
from .interpreter import NodeInterpreter as _NodeInterpreter


class Context(_NodeInterpreter):

    def exec(self, code: _Union[str, bytes]):
        if isinstance(code, str):
            code = code.encode("utf-8")
        super().exec(code)

    def eval(self, code: _Union[str, bytes]):
        if isinstance(code, str):
            code = code.encode("utf-8")
        return super().eval(code)


def compile_(code: _Union[str, bytes]) -> Context:
    if isinstance(code, str):
        code = code.encode("utf-8")

    ctx = Context()
    ctx.exec(code)
    return ctx
