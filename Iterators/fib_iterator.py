class FibIterator:

    def __init__(self, stop=20):
        self.stop = stop

    def __iter__(self):
        self.n = 0
        self.a = 1
        self.i = 1
        return self

    def __next__(self):
        if self.i <= self.stop:
            self.n, self.a = self.a, self.n + self.a
            self.i += 1
            return self.n
        else:
            raise StopIteration


for n in FibIterator(40):
    print(n)