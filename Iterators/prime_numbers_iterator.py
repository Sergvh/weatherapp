class PrimeIterator:

    def __init__(self, stop=20):
        self.stop = stop

    def __iter__(self):
        self.n = 3
        return self

    def __next__(self):
        result = 0
        if self.n < self.stop:
            for i in range(2, self.n):
                if self.n % i == 0:
                    break
            else:
                result = self.n
            self.n += 1
            return result
        else:
            raise StopIteration


for k in PrimeIterator(100):

    if k != 0:
        print(k)
