class frange:
    def __init__(self, *args, start=0, end=0, step: float = 1.0):
        if len(args) == 1:
            self._start, self._step = start, step
            self._end = args[0]
        elif len(args) == 2:
            self._start, self._end = args
            self._step = step
        else:
            self._start, self._end, self._step = args

    def __iter__(self):
        return self

    def __next__(self):
        if (self._start >= self._end and self._step > 0) \
                or (self._start <= self._end and self._step < 0):
            raise StopIteration('Limit is exceeded')
        value = self._start
        self._start += self._step
        return value


if __name__ == '__main__':
    assert (list(frange(5)) == [0, 1, 2, 3, 4])
    assert (list(frange(2, 5)) == [2, 3, 4])
    assert (list(frange(2, 10, 2)) == [2, 4, 6, 8])
    assert (list(frange(10, 2, -2)) == [10, 8, 6, 4])
    assert (list(frange(2, 5.5, 1.5)) == [2, 3.5, 5])
    assert (list(frange(1, 5)) == [1, 2, 3, 4])
    assert (list(frange(0, 5)) == [0, 1, 2, 3, 4])
    assert (list(frange(0, 0)) == [])
    assert (list(frange(100, 0)) == [])

    print('SUCCESS!')
