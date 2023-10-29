import time

def timeit(f):
    def wrapper(*args, **kwargs):
        print(f"calling {f} with {args}")
        t0 = time.monotonic_ns()
        f(*args, **kwargs)
        t1 = time.monotonic_ns()
        print(f"{f} call took {t1-t0} ns")
    return wrapper

class Multitime:
    average = 0
    ncalls = 0
    tmin = None
    tmax = 0
    tlast = 0
    lastargs = None
    lastkwargs = None
    
    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        t0 = time.monotonic_ns()
        result = self.f(*args, **kwargs)
        t1 = time.monotonic_ns()
        self.average = (self.average + (t1-t0)) / self.ncalls
        if t1-t0 > self.tmax:
            self.tmax = t1-t0
        if not self.tmin or t1-t0 < self.tmin:
            self.tmin = t1-t0
        self.tlast = t1-t0
        self.lastargs = args
        self.lastkwargs = kwargs
        return result
        
    def __init__(self, f):
        self.f = f

    def print_res(self):
        print(f"{self.f.__name__}: average"\
              f" {self.average:.2f}ns across {self.ncalls} calls, ",
              end="")
        print(f"min = {self.tmin}ns, max = {self.tmax}ns")

    def print_last(self):
        print(f"last call {self.f.__name__}(", end="")
        for k in self.lastargs:
            print(f"{k},", end="")
        for k, v in self.lastkwargs:
            print(f"{k}={v},", end="")
        print(f") took {self.tlast}ns")




@Multitime
def test(s, x):
    return s**s+x

test(0.1, 1)
test.print_last()
test(0, 1)
test.print_last()
test(1, 4)
test(4, 4)
test(100, 4)
test(1234, 4)
test.print_last()


test.print_res()

@Multitime
def ack(m, n):
   if m==0: return n+1
   if m>0 and n==0: return ack(m-1, 1)
   if m>0 and n>0: return ack(m-1, ack(m, n-1))


print(ack(2, 2))
ack.print_last()
print(ack(3, 3))
ack.print_last()
print(ack(3, 4))
ack.print_last()
print(ack(3, 1))
ack.print_last()
# ack(4, 4) przepełnia stos
ack.print_res()
