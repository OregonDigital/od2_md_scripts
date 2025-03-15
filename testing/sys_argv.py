import sys
# can't remember if 'python'/'python3' is counted in indexing
# run $ 'python3 sys_argv.py' + arbitrary number of additional arbitrary args
print("arguments indexed by sys.argv:")
for arg in sys.argv:
    print(f"{sys.argv.index(arg)}: {arg}")
