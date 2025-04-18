from __future__ import annotations
__package__ = "pytwojs"

import json
import subprocess
import typing
import threading
import time
import uuid
import weakref

from .utils import make_cmd
from .exceptions import JSException
from ._program import EXEC_END_FLAGS, EXEC_DONE_FLAGS


def _generate_name() -> str:
    return f"__{str(int(time.time() * 1000000))}{uuid.uuid4().hex[:16]}"


def _close(node) -> None:
    return_code = node.poll()
    if return_code is None:
        node.stdin.close()
        node.stdout.close()
        node.wait()


class NodeInterpreter:

    def __init__(self) -> None:
        cmd = make_cmd()
        self._node = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._global_interpreter_lock = threading.Lock()
        self._finalizer = weakref.finalize(self, _close, self._node)

    def exec(self, code: bytes) -> None:
        """
        Execute the given JavaScript code(multi line)
        :param code: bytes
        :return: None
        """
        with self._global_interpreter_lock:
            self._write(code + b"\n")
            self._flush()
            self._write(EXEC_END_FLAGS)
            self._flush()
            while out := self._readline():
                try:
                    out_obj = json.loads(out)
                    if isinstance(out_obj, dict):
                        if out_obj.get("stringify") == EXEC_DONE_FLAGS:
                            break
                except json.JSONDecodeError:
                    pass

    def eval(self, code: bytes) -> JSProxyWrapper:
        """
        Execute single line JS expression or Get JavaScript object
        :param code: JavaScript single line expression
        :return: JSProxyWrapper
        """
        with self._global_interpreter_lock:
            self._write(code + b"\n")
            self._flush()
            result = self._reach_result_line()

        if result[:8] == b"Uncaught":
            py_obj = json.loads(result.removeprefix(b"Uncaught").strip())
            raise JSException(py_obj['toString'])

        return JSProxyWrapper(self, result, code.strip())

    def _reach_result_line(self) -> bytes:
        while out := self._readline():
            out_cpy = out.strip()
            if out_cpy[:8] == b"Uncaught":
                return out_cpy
            try:
                pyobj = json.loads(out_cpy)
                if isinstance(pyobj, dict):
                    if len(pyobj.keys()) == 3:
                        try:
                            _ = pyobj['stringify'] and pyobj['toString'] and pyobj['exception']
                            return out_cpy
                        except KeyError:
                            pass
            except json.JSONDecodeError:
                pass

    @property
    def is_closed(self):
        return_code = self._node.poll()
        if return_code is not None:
            return True
        return False

    def close(self) -> None:
        self._finalizer()

    def _write(self, code: bytes):
        self._node.stdin.write(code)

    def _flush(self):
        self._node.stdin.flush()

    def _readline(self):
        return self._node.stdout.readline()

    def __enter__(self) -> NodeInterpreter:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self):
        self.close()


class JSProxyWrapper:

    def __init__(self, node: NodeInterpreter, js_result: bytes, name: bytes) -> None:
        self._node_repl = node
        self._js_result = js_result
        self._name = name
        self._lock = node._global_interpreter_lock

    def _eval(self, code: bytes, is_obj=False) -> JSProxyWrapper:
        with self._lock:
            if not is_obj:
                self._node_repl._write(self._name + b"." + code + b"\n")
            else:
                name = _generate_name().encode("utf-8")
                self._node_repl._write(name + b"=" + code + b"\n")
            self._node_repl._flush()
            result = self._node_repl._reach_result_line()

        if result[:8] == b"Uncaught":
            pyobj = json.loads(result.removeprefix(b"Uncaught").strip())
            raise JSException(pyobj['toString'])

        if not is_obj:
            return JSProxyWrapper(self._node_repl, result, self._name + b"." + code.strip())
        return JSProxyWrapper(self._node_repl, result, name)

    def call(self, func: str, *args) -> JSProxyWrapper:
        """Call functions within the object itself"""
        call_js_str = f"{func}(...{json.dumps(args)})".encode("utf-8")
        return self._eval(call_js_str)

    def __getattr__(self, name) -> JSProxyWrapper:
        return self._eval(name.encode('utf-8'))

    def __call__(self, *args, **kwargs) -> JSProxyWrapper:
        pyobj = json.loads(self._js_result)
        if pyobj['toString'][1:14] == "AsyncFunction":
            call_js_str = f"(await {self._name.decode('utf-8')}(...{json.dumps(args)}))".encode("utf-8")
        elif pyobj['toString'][1:6] == "class":
            call_js_str = f"new {self._name.decode('utf-8')}(...{json.dumps(args)})".encode("utf-8")
        else:
            call_js_str = f"{self._name.decode('utf-8')}(...{json.dumps(args)})".encode("utf-8")

        return self._eval(call_js_str, True)

    @property
    def _value(self) -> bytes:
        return self._js_result

    @property
    def pyobj(self) -> typing.Any:
        """Get python object"""
        result = json.loads(self._js_result)
        if result['stringify'] == "undefined":
            return None

        return result['stringify']
