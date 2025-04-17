# co_code = b'\x88\x00\x7c\x00\x7c\x01\x8e\x01\x7d\x02\x7c\x02\x53\x00'

# def _hash(bytes) -> int:
#     # print(bytes)
#     hash = 0
#     # hash = hash + int(bytes)
#     return hash

# def compute_line_hash(block_hash, linenum):
#     # print(type(block_hash))
#     # print(block_hash, linenum)
#     return block_hash ^ linenum

# for line_num, byte in zip([61]*10 + [62]*4,co_code):
#     code_hash = compute_line_hash(_hash((co_code)), line_num)
#     # print byte in binary
#     print(byte, bin(byte), hex(byte))
#     # println!("Offset: {}, Byte: {:#04x}, Line: {}", offset, byte, line_no);
#     # print(code_hash)

# for offset, byte in enumerate(co_code):
#     PyCode_Addr2Line(<PyCodeObject*>code, offset)
#     code_hash = compute_line_hash(hash(co_code)), )
#     if not self._c_code_map.count(code_hash):
#         try:
#             self.code_hash_map[code].append(code_hash)
#         except KeyError:
#             self.code_hash_map[code] = [code_hash]
#         self._c_code_map[code_hash]

# self.functions.append(func)

import sys

def function():
    x=1
    try:
        assert 1==2
    except Exception as e:
       x=e
    return x

def trace(frame, event, arg):
    """
        frame:frame 是当前堆栈帧
        event:一个字符串，可以是'call', 'line', 'return', 'exception'或者'opcode'
        arg:取决于事件类型

            frame.f_code.co_name  执行函数名称
            frame.f_lineno   执行行号
            frame.f_locals["arr"]
    """
    print(event, frame.f_code.co_name, frame.f_lineno,"==>", frame.f_locals, arg)
    return trace

sys.settrace(trace)
print(123)
for i in range(10):
    function() 
print(456)
sys.settrace(None)
from inspect import getmembers
for k, v in getmembers(function.__code__):
    print(k,v)
print(function.__code__.co_filename)
print(function.__code__.co_firstlineno)