def countTen(num=5, stop=10):
    print("called the first time\n")
    i = 0
    while i <= stop:
        yield i + num
        i += 1
    print("\n called the last time\n")


count = countTen(10, 10)

try:
    while True:
        print(next(count))
except StopIteration:
    pass
