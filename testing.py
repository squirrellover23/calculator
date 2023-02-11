class test:

    def __init__(self, x):
        self.val = x

    def __add__(self, other):
        self.val += other

        return self

    def __str__(self):
        return str(self.val)

    def __int__(self):
        return self.val


x = 9.8

print(x % 1)

