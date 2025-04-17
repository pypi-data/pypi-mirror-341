core feature:
1. Profiling by line

time every single line
kernprof will create an instance of LineProfiler and insert it into the __builtins__ namespace with the name profile. It has been written to be used as a decorator, so in your script, you decorate the functions you want to profile with @profile.

2.
no decorator needed
@profile

3. trace the sub if time functions > 20% and output to dict
every func will spawn a new rust thread ,

unit in ns (1e-9)


4. vscode extension