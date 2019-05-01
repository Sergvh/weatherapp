def prime_generator(stop=10):
    i = 0
    result = 0
    while i <= stop:
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            result = i
        i += 1
        yield result


prime = prime_generator(30)
try:

    r = 0
    while True:
        k = next(prime)
        if k != r:
            print(k)
            r = k

except StopIteration:
    pass
