import math







class poly_term:
    def __init__(self, variable_symbol, cof, power):
        self.symbol = variable_symbol
        self.cof = cof
        self.power = power

    def __str__(self):
        power_sym = f'{self.symbol}^{str(self.power)}'
        if self.cof == 1 and self.power == 0:
            return '1'
        if self.power == 0 and self.cof == 0:
            return '0'

        if self.power == 1:
            power_sym = str(self.symbol)
        elif self.power == 0:
            power_sym = ''
        if self.cof == 0:
            return ''
        elif self.cof == 1:
            return power_sym
        return f'{str(self.cof)}{power_sym}'

    def __add__(self, other):
        if type(other) == poly_term:
            if other.symbol == self.symbol:
                if self.power == other.power:
                    return poly_term(self.symbol,  self.cof + other.cof, self.power)
        else:
            new = single_var_polynomial(self.symbol, [])
            new += self
            new += other
            return new

    def __mul__(self, other):
        if type(other) == poly_term:
            if other.symbol == self.symbol:
                return poly_term(self.symbol, self.cof * other.cof, self.power + other.power)
        else:
            return poly_term(self.symbol, other * self.cof, self.power)

    def value(self, val):
        return self.cof * pow(val, self.power)


# polynomial is a list [[cof, power], ...] for all the terms of the polynomial

class single_var_polynomial:
    def __init__(self, var, polynomial, poly_object=None):
        if poly_object is not None:
            self.polynomial = []
            for i in poly_object.polynomial:
                self.polynomial.append(poly_term(var, i.cof, i.power))
            self.var = poly_object.var
        else:
            self.polynomial = []
            self.var = var
            for i in polynomial:
                if i[1] > len(self.polynomial)-1:
                    for b in range(i[1]-len(self.polynomial)+1):
                        if len(self.polynomial) == 0:
                            power = 0
                        else:
                            power = self.polynomial[-1].power + 1
                        self.polynomial.append(poly_term(self.var, 0, power))
                self.polynomial[i[1]] = self.polynomial[i[1]] + poly_term(self.var, i[0], i[1])
        self.update()

    def update(self):
        if len(self.polynomial) != 0:
            if self.polynomial[-1].power + 1 != len(self.polynomial):
                print('fail')
        checking = True
        while checking:
            if len(self.polynomial) == 0 or 1:
                checking = False

            elif self.polynomial[-1].cof == 0:
                self.polynomial.pop(-1)
            else:
                checking = False
        self.order = len(self.polynomial) - 1




    def __add__(self, other):
        if type(other) == poly_term:
            if other.power > len(self.polynomial) - 1:
                for b in range(other.power - len(self.polynomial) + 1):
                    if len(self.polynomial) == 0:
                        power = 0
                    else:
                        power = self.polynomial[-1].power + 1
                    self.polynomial.append(poly_term(self.var, 0, power))
            self.polynomial[other.power] = self.polynomial[other.power] + other
            self.update()
            return single_var_polynomial(self.var, [], self)

        elif type(other) == single_var_polynomial:
            if len(other.polynomial) > len(self.polynomial):
                for b in range(len(other.polynomial) - len(self.polynomial)):
                    if len(self.polynomial) == 0:
                        power = 0
                    else:
                        power = self.polynomial[-1].power + 1
                    self.polynomial.append(poly_term(self.var, 0, power))
            for i in other.polynomial:
                self.polynomial[i.power] = self.polynomial[i.power] + i
            return single_var_polynomial(self.var, [], self)

        if type(other) == int or float:
            self += poly_term(self.var, other, 0)
            self.update()
            return self

    def __mul__(self, other):
        if type(other) == single_var_polynomial:
            new_poly = single_var_polynomial(self.var, [[0, 0]])

            for i in self.polynomial:
                new_poly += other * i
            return new_poly

        elif type(other) == poly_term:

            if other.symbol == self.var:
                new_poly = single_var_polynomial(self.var, [], self)

                for i in range(other.power):
                    new_poly.polynomial.append(poly_term(self.var, 0, self.polynomial[-1].power + 1))

                for i in range(0, len(self.polynomial) + other.power):
                    if i > len(self.polynomial)-1:
                        new_poly.polynomial[-i-1] = self.polynomial[0] * 0
                    else:
                        new_poly.polynomial[self.polynomial[i].power+other.power] = self.polynomial[i] * other

                return new_poly
        else:
            new_poly = single_var_polynomial(self.var, [])

            for i in self.polynomial:
                new_poly += i * other
            return new_poly

    def __imul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        for i in range(power-1):
            self *= self
        return self

    def __iadd__(self, other):
        return self + other

    def __str__(self):
        self.update()
        ret = ''
        for i in range(len(self.polynomial)):
            ret += str(self.polynomial[-i - 1])
            if i != len(self.polynomial)-1 and str(self.polynomial[-i-1]) != '':
                ret += ' + '

        return ret

    def solve_for_roots(self):
        self.update()
        checking = True
        new_num = -1
        while checking:
            if self.polynomial[-1].cof == 0:
                self.polynomial.pop(-1)
            else:
                checking = False

        self.roots = []
        self.order = len(self.polynomial) - 1

        p = self.polynomial
        if self.order == 2:
            root_part = -1 * p[1].cof
            num = p[1].cof * p[1].cof + (-4 * p[0].cof * p[2].cof)

            if num >= 0:
                self.roots.append((root_part + math.sqrt(num)) / (2 * p[2].cof))
                self.roots.append((root_part - math.sqrt(num)) / (2 * p[2].cof))
        else:
            self.fprime = self.find_dirivative()
            n1 = .1
            while abs(self.calculate_value(n1)) > 0.000000001:
                n = n1
                n1 = n - self.calculate_value(n) / self.fprime.calculate_value(n)

            n1 = int(100 * n1 + .5)
            n1 /= 100
            self.roots.append(n1)
            s = self.synthetic_divide(n1)

            if s.order != 0:

                self.roots += s.solve_for_roots()
        return self.roots

    def find_dirivative(self):
        new_poly = single_var_polynomial(self.var, [])
        for i in self.polynomial:
            if i.power - 1 >= 0:
                new_poly += poly_term(self.var, i.cof * i.power, i.power - 1)
        return new_poly

    def calculate_value(self, value):
        ret_val = 0
        for i in self.polynomial:
            ret_val += i.value(value)

        return ret_val

    def synthetic_divide(self, root):
        a = 0
        new_poly = single_var_polynomial(self.var, [])
        for b in range(1, len(self.polynomial) + 1):
            i = self.polynomial[-b]
            a *= root
            a += i.cof
            if b == len(self.polynomial):
                if i.power >= 0.0001:
                    print('HOUSTAN WE HAVE AN ERROR')
            else:
                new_poly += poly_term(self.var, a+0, i.power-1)
        return new_poly


