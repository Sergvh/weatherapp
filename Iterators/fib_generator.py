def fib_generator(stop=30):
    i = 0
    a, b = 0, 1
    yield 0
    while i < stop:
        a, b = b, a + b
        i += 1
        yield a


fib = fib_generator(40)

try:
    while True:
        print(next(fib))
except StopIteration:
    pass
