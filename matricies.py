from polynomial import single_var_polynomial

matrix_3 = [
    [11, 12, 13],
    [21, 22, 23],
    [31, 32, 33]
]


matrix_4 = [
    [2, 0, 0, -1],
    [0, 1, 4, 0],
    [0, 2, 3, 0],
    [1, 0, 0, 1]
]



class elementary_product:

    def __init__(self, product):
        self.product = [None] * len(product)
        for i in product:
            self.product[i.pos_x-1] = i
        num = 0
        even_odd_num = 0
        even_odd_list = []
        for i in self.product:
            num += 1
            for b in even_odd_list:
                if i.pos_y < b.pos_y:
                    even_odd_num += 1

            even_odd_list.append(i)
        if even_odd_num % 2 == 0:
            self.sign = 1
        else:
            self.sign = -1
        self.val = 1
        for i in self.product:
            self.val = i * self.val
        self.val *= self.sign

    def __str__(self):
        if self.sign < 0:
            response = '-('
        else:
            response = '('
        for i in self.product:
            response += str(i.pos_y)
            if self.product[-1] != i:
                response += ', '
        response += ')'
        return response

    def __int__(self):
        return self.val

    def __add__(self, other):
        return self.val + other


class matrix_entry:

    def __init__(self, pos_x, pos_y, value):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __mul__(self, other):
        return self.value * other

    def __imul__(self, other):
        return self * other

class matrice:

    def __init__(self, matrix):
        self.matrix = []
        cnum = -1
        for i in matrix:
            cnum += 1
            self.matrix.append([])
            rnum = -1
            for b in i:
                rnum += 1
                self.matrix[cnum].append(matrix_entry(cnum + 1, rnum + 1, b))
        self.height = len(self.matrix)
        self.width = len(self.matrix[0])
        self.square = (self.width == self.height)
        if self.square:
            self.elementary_products = []
            self.loop_through_matrix(self.matrix, [], 0)

            self.find_determinate()

        else:
            self.det = None
            self.elementary_products = None

    def __add__(self, other):
        if type(other) == matrice and other.height == self.height and other.width == self.width:
            new_matrix = []
            numr = -1
            for i in self.matrix:
                numr += 1
                numc = -1
                new_matrix.append([])
                for b in i:
                    numc += 1
                    new_matrix[numr].append(b.value + other.matrix[numr][numc].value)
            return matrice(new_matrix)


    def __mul__(self, other):
        new_matrix = []
        if type(other) == matrice:
            if other.height == other.width:
                pass
                #multiply matricies
        else:
            num = -1
            for i in self.matrix:
                num += 1
                new_matrix.append([])
                for b in i:
                    try:
                        new_matrix[num].append(other * b)
                    except TypeError:
                        new_matrix[num].append(b * other)
        return matrice(new_matrix)

    def __str__(self):
        ret = ''
        for i in self.matrix:
            ret += '[ '
            for b in i:

                if type(b.value) == single_var_polynomial and str(b.value).count(b.value.var) > 0:
                    r = f'({str(b)})'
                else:
                    r = str(b)
                if b == i[-1]:
                    ret += r + ' ]\n'
                else:
                    ret += r + ' '
        return ret

    def find_determinate(self):
        self.det = 0
        for i in self.elementary_products:
            self.det = i + self.det

    def loop_through_matrix(self, matrix, el_product, pos_in_values):
        if len(matrix) <= 1:
            if len(el_product) < pos_in_values + 1:
                el_product.append(matrix[0][0])
            else:
                el_product[pos_in_values] = matrix[0][0]
            self.elementary_products.append(elementary_product(el_product))

        else:
            i = matrix[0]
            for a in range(0, len(i)):
                if len(el_product) < pos_in_values + 1:
                    el_product.append(i[a])
                else:
                    el_product[pos_in_values] = i[a]

                temp_matrix = []
                num = -1
                for t in matrix:
                    temp_matrix.append([])
                    num += 1
                    for r in t:
                        temp_matrix[num].append(r)
                del temp_matrix[matrix.index(i)]
                for b in range(0, len(temp_matrix)):
                    del temp_matrix[b][a]
                self.loop_through_matrix(temp_matrix, el_product, pos_in_values + 1)

    def find_eign_vals(self):
        if self.square:
            lamb = single_var_polynomial('lamb', [[1, 1]])
            c = I(self.width) * lamb
            c = c + (self * -1)
            self.eigen_vals = c.det.solve_for_roots()
            print(self.eigen_vals)



def I(n):
    matrix = []
    for i in range(0, n):
        matrix.append([])
        for b in range(0, n):
            if i != b:
                matrix[i].append(0)
            else:
                matrix[i].append(1)
    return matrice(matrix)


m = matrice(matrix_4)
print(m)
m = m + I(4)
m.find_eign_vals()
