import inspect
from types import FunctionType, CodeType
import re

FUNCTION = "function"
FUNCTION_ATTRIBUTES = [
    "__code__",
    "__name__",
    "__defaults__",
    "__closure__",
]

CODE_FIELD = "__code__"
GLOBALS = "__globals__"

GLOBALS_FIELDS = 'co_names'
CODE_ARGS = (
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
)

TYPE_FIELD = "TYPE"
VALUE_FIELD = "VALUE"

CLASS_TYPE_REGEX = "\'([\w\W]+)\'"


def serialize_obj(obj):
    result = dict()
    t = type(obj)
    type_string = re.search(CLASS_TYPE_REGEX, str(t)).group(1)
    if t == dict:
        for name, value in obj.items():
            result[name] = serialize_obj(value)
    elif t == list or t == tuple:
        result[TYPE_FIELD] = type_string
        result[VALUE_FIELD] = list()
        for value in obj:
            result[VALUE_FIELD].append(serialize_obj(value))
    elif inspect.isroutine(obj):
        result[TYPE_FIELD] = type_string
        result[VALUE_FIELD] = serialize_func(obj)
    elif t == bytes:
        result[TYPE_FIELD] = type_string
        result[VALUE_FIELD] = list(obj)
    elif isinstance(obj, (int, float, complex, bool, str)) or obj is None:
        return obj
    else:
        result[TYPE_FIELD] = type_string
        result[VALUE_FIELD] = serialize_instance(obj)
    return result


def serialize_func(func):
    result = {}
    details = inspect.getmembers(func)
    for detail in details:
        if inspect.isbuiltin(detail[1]):
            continue
        if detail[0] in FUNCTION_ATTRIBUTES:
            result[detail[0]] = serialize_obj(detail[1])
            if detail[0] == CODE_FIELD:
                result[GLOBALS] = {}
                glob = func.__getattribute__(GLOBALS)
                for name in detail[1].__getattribute__(GLOBALS_FIELDS):
                    if name == func.__name__:
                        result[GLOBALS][name] = func.__name__
                        continue
                    if name in __builtins__:
                        continue
                    if name in glob:
                        if inspect.ismodule(glob[name]):
                            continue
                        result[GLOBALS][name] = serialize_obj(glob[name])
    return result


def serialize_instance(inst):
    result = dict()
    attrs = inspect.getmembers(inst)
    for attr in attrs:
        if callable(attr[1]):
            continue
        result[attr[0]] = serialize_obj(attr[1])
    return result


def deserialize_obj(obj):
    t = type(obj)
    if t == dict:
        result = {}
        if VALUE_FIELD in obj and TYPE_FIELD in obj:
            return deserialize_inst(obj[TYPE_FIELD], obj[VALUE_FIELD])
        for name, o in obj.items():
            tp = type(o)
            if tp == dict:
                result[name] = deserialize_obj(o)
            else:
                result[name] = o
        return result
    return obj


def deserialize_func(func):
    code_fields = func[CODE_FIELD][VALUE_FIELD]
    code_args = []
    for field in CODE_ARGS:
        arg = code_fields[field]
        if type(arg) == dict:
            if arg[TYPE_FIELD] == "bytes":
                code_args.append(bytes(arg[VALUE_FIELD]))
            else:
                code_args.append(tuple(arg[VALUE_FIELD]))
        else:
            code_args.append(arg)
    details = [CodeType(*code_args)]
    glob = {"__builtins__": __builtins__}
    for name, o in func[GLOBALS].items():
        glob[name] = deserialize_obj(o)
    details.append(glob)
    for attr in FUNCTION_ATTRIBUTES:
        if attr == CODE_FIELD:
            continue
        details.append(deserialize_obj(func[attr]))

    result_func = FunctionType(*details)
    if result_func.__name__ in result_func.__getattribute__(GLOBALS):
        result_func.__getattribute__(GLOBALS)[result_func.__name__] = result_func
    return result_func


def deserialize_inst(key, value):
    if key == "tuple":
        return tuple(value)
    elif key == "function":
        return deserialize_func(value)
    else:
        return value
