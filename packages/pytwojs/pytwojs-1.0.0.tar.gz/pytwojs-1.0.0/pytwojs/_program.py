PROGRAM = """
const repl = require('node:repl');
function toString(obj){return Object.prototype.toString.call(obj)}
function isClass(obj) {
  if (typeof obj !== 'function') return false;
  if (!obj.prototype) return false;
  const descriptor = Object.getOwnPropertyDescriptor(obj, 'prototype');
  if (descriptor?.writable !== false) return false;
  let isCallable = false
  try {
    Reflect.construct(obj, [], obj);
    isCallable = true
  } catch (e) {
    return false;
  }
  const isNativeClass = Function.prototype.toString.call(obj).startsWith('class');
  const isBuiltin = obj.name in globalThis;
  return isNativeClass || isBuiltin || isCallable;
}
const replServer = repl.start({
  prompt: '',
  writer: (output) => {
    switch (toString(output)) {
      case "[object Undefined]":
        return `{"stringify":"${JSON.stringify(output)}","toString":"${toString(output)}","exception":0}`;
      case "[object Error]":
        return `{"stringify":${JSON.stringify(output)},"toString":"${output.toString()}","exception":1}`;
      case "[object Function]":
        if (!isClass(output))
          return `{"stringify":"${JSON.stringify(output)}","toString":"[Function: ${output.name}]","exception":0}`;
        return `{"stringify":"${JSON.stringify(output)}","toString":"[class ${output.name}]","exception":0}`;
      case "[object AsyncFunction]":
        return `{"stringify":"${JSON.stringify(output)}","toString":"[AsyncFunction: ${output.name}]","exception":0}`;
    }
    try {
      return `{"stringify":${JSON.stringify(output)},"toString":"${output.toString()}","exception":0}`;
    } catch (e) {
      return `{"stringify":"${toString(output)}","toString":"${toString(output)}","exception":0}`;
    }
  }
});
"""

FLAGS = "-e"
EXEC_END_FLAGS = b"'[[[______<<<exec_done>>>______]]]'\n"
EXEC_DONE_FLAGS = "[[[______<<<exec_done>>>______]]]"
