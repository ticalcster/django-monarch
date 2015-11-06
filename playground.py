class A(object):
    def __new__(cls, *args, **kwargs):
        new_class = super(A, cls).__new__(cls, *args)
        if 'one' in kwargs:
            new_class.one = kwargs.get('one')
        return new_class

    def __init__(self, *args, **kwargs):
        print('----', 'test')


class B(object):
    def __init__(self, num):
        self.num = num

    def fetch(self):
        current = 0
        while current < self.num:
            yield current
            current += 1

    def fetch_all(self):
        l = []
        current = 0
        while current < self.num:
            l.append(current)
            current += 1
        return l


