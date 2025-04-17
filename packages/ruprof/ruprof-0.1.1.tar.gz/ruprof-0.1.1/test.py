from ruprof import Profiler
from sys import byteorder
import opcode
# from line_profiler import LineProfiler as Profiler

NOP_VALUE: int = opcode.opmap['NOP']

profile = Profiler()
NOP_BYTES: bytes = NOP_VALUE.to_bytes(2, byteorder=byteorder)
dupes_map = {}
_c_code_map = {}

def _code_replace(func, co_code):
    """
    Implements CodeType.replace for Python < 3.8
    """
    try:
        code = func.__code__
    except AttributeError:
        code = func.__func__.__code__
    if hasattr(code, 'replace'):
        # python 3.8+
        code = code.replace(co_code=co_code)
    return code

def decorator2(func):
    code = func.__code__
    # code = func.__func__.__code__
    print(code)
    print(type(code))
    co_code = code.co_code
    print(co_code)
    print(type(co_code))
    if code.co_code in dupes_map:
        dupes_map[code.co_code] += [code]
        co_padding : bytes = NOP_BYTES * (len(dupes_map[code.co_code]) + 1)
        co_code = code.co_code + co_padding
        CodeType = type(code)
        code = _code_replace(func, co_code=co_code)

        try:
            func.__code__ = code
        except AttributeError as e:
            func.__func__.__code__ = code
    else:
        dupes_map[code.co_code] = [code]
    print("dupes map: ", dupes_map)
    print(hash(code.co_code))
    # for offset, byte in enumerate(code.co_code):
    #     code_hash = compute_line_hash(hash((code.co_code)), PyCode_Addr2Line(<PyCodeObject*>code, offset))
    #     if not _c_code_map.count(code_hash):
    #         try:
    #             code_hash_map[code].append(code_hash)
    #         except KeyError:
    #             code_hash_map[code] = [code_hash]
    #         _c_code_map[code_hash]

    # self.functions.append(func)

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

# @decorator2
def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

class funcs():
    def __init__(self):
        pass
    @profile
    def my_function(x):
        total = 0
        for i in range(x):
            total += i
        return total

    @profile
    def another_function(x):
        return x * x

for i in range(10000):
    funcs.my_function(200)
    # print("YYYYY")
    funcs.another_function(10)
    # print("ZZZZ")


try:
    profile.print_stats()
except Exception as e:
    prof = profile.get_stats()
    # {'0x7f737d3981b0:68': {'count': 1000, 'time': 0.001660382000000008}, '0x7f737d3981b0:79': {'count': 1000, 'time': 0.0012413379999999946}, '0x7f737d3981b0:76': {'count': 1000, 'time': 0.0017175539999999944}, '0x7f737d3981b0:78': {'count': 1001, 'time': 0.0028143760000000208}, '0x7f737d3981b0:81': {'count': 1000, 'time': 0.002920404000000002}, '0x7f737d3981b0:69': {'count': 11000, 'time': 0.01229601999999817}, '0x7f737d3981b0:75': {'count': 1, 'time': 1.64e-06}, '0x7f737d3981b0:74': {'count': 1, 'time': 3.2e-07}, '0x7f737d3981b0:70': {'count': 10000, 'time': 0.011394422999998908}, '0x7f737d3981b0:85': {'count': 1, 'time': 1.39e-06}, '0x7f737d3981b0:72': {'count': 1000, 'time': 0.0010990519999999988}}
    # sort by line numbers
    for k in sorted(prof, key=lambda x: x.split(":")[1]):
        stat = prof[k]
        print(k, stat['count'], stat['time'], sep="\t")


# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# from inspect import getmembers
# for k, v in getmembers(my_function):
#     print(k,v)

# print(my_function.__code__.co_filename)
# print(another_function.__code__.co_filename)

"""
Timer unit: 1e-09 s

Total time: 0.156564 s
File: test.py
Function: sum at line 3

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           @profiler
     4                                           def sum(a,b):
     5   1000000  156563981.0    156.6    100.0      return a + b
"""

# RuProf Development
# docker run --name ruprof --rm -it -v $PWD:/w -w /w rust-python bash
# uv venv --python 3.8
# source .venv/bin/activate
# uv add astor line_profiler
# clear && maturin develop && python3 test.py

# line_profiler
# docker run --name ruprof --rm -it -v $PWD:/w -w /w rust-python bash
# uv pip install line_profiler
# source .venv/bin/activate
# python3 test.py

# RuProf Deployment
# docker run --name ruprof --rm -it -v $PWD:/w -w /w rust-python bash
# source .venv/bin/activate
# clear && maturin develop --release && python3 test.py 1