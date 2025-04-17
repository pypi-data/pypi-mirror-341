import sys
DEV = len(sys.argv) >= 2
if DEV:
    from ruprof import Profiler
    profile = Profiler()
else: 
    from line_profiler import LineProfiler
    profile = LineProfiler()

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
    my_function(1000)
    another_function(2000)


if DEV:
    print(profile.get_stats())
else:
    profile.print_stats()

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
# source .venv/bin/activate
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