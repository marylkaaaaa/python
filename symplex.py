SHOW_PROCESS = True
import numpy


def print_iter_matr(A, f):
    iter_matr = zip(A,f)
    iter_matr = list(iter_matr)
    for el in iter_matr:
        j = 1
        for nel in el[0]:
            print('{} * x{} '.format(nel, j), end='')
            if j != len(el[0]):
                print('+ ', end=' ')
            j += 1
        print('= ', el[1])


def less_then(i, m):
    # <=: добавляется базисная переменная со знаком "+"
    # возвращает масив из м елементов с 1 на итом месте, вид переменной (базис) и входимость в базис(да)

    var = [0] * m
    var[i] = 1.0
    return [var], ["b"], [True]


def greater_then(i, m):
    # >= - базисная переменная со знаком "-" и временная переменная со знаком "+"
    # возвращает масив из м елементов с -1 на итом месте, вид переменной (базис) и входимость в базис(нет)
    # и масив из м елементов с 1 на итом месте, вид переменной (врем) и входимость в базис(да)

    var1 = [0] * m
    var1[i] = -1.0
    var2 = [0] * m
    var2[i] = 1.0
    return [var1, var2], ["b", "t"], [False, True]


def equal_to(i, m):
    # = - временная переменная со знаком "+"
    # возвращает масив из м елементов с 1 на итом месте, вид переменной (врем) и входимость в базис(да)
    var = [0] * m
    var[i] = 1.0
    return [var], ["t"], [True]


def symplex_method(A, f, I, k):
    # словарь действий при знаке
    sign_change = {"<=": less_then, ">=": greater_then, "=": equal_to}
    # количество ограничений
    m = len(A)
    # количество базисных переменных
    n = len(A[1])
    # начальные оценки
    k = map(lambda x: -x, k)

    # масив н+м, где для базисных записан номер строки, а для остальных - -1
    which_str = [-1] * n
    # масив типов переменных
    type_var = ["f"] * n
    # список добавочных векторов
    add = []

    # считает строку базисных переменных
    # НАЙТИ КНИГУ
    class Counter():
        cnt = -1

        def inc(self):
            self.cnt = self.cnt + 1
            return self.cnt

    cnt = Counter()

    # канонический вид (с равно и доп переменными)
    i = 0
    for el in I:
        func = sign_change[I[i]]
        arr, t_var, basic = func(i, m)
        #print(el, ' ' , t_var, basic)

        # если переменная базисная (true), запоминаем строку
        which_str = which_str + [(cnt.inc() if letter else -1) for letter in basic]
        type_var = type_var + t_var
        add = add + arr
        i += 1

    len_which_str = len(which_str)
    len_add = len(add)
    tr_add = numpy.transpose(add)
    # print(tr_add)

    for i in zip(type_var, which_str):
        print(i)

    # матрица коеф по строкам для всех переменных
    new_A = []
    for i in enumerate(tr_add):
        n = list(tr_add[i[0]])
        new = A[i[0]] + n
        new_A.append(new)

    #print(new_A)

    # для новых переменных коеф цел функции - 0
    new_k = list(k)
    new_k = new_k + [0] * len_add

    # начальное знач целевой функции
    F = 0

    iter_number = 0

    if SHOW_PROCESS:
        print('\nIteration number: {}\n'.format(iter_number))
        print_iter_matr(new_A, f)

        # до конца решения
        while 1:
            '''
            находим разрешающий столбец - столбец, в котором целевая функция имеет 
            наименьший параметр (наибольший по модулю)
            переменная из разрешающего столбца попадает в базис при следующей итерации

            если на данной итерации в базисе участвуют временные переменные, то 
            всместо строки z необходимо рассматривать оценку, в которой участвуют 
            только строки таблцы, соответвующие временным переменным

            получаем переменные, участвующие в текущей итерации в качестве базиса
            и узнаем их тип
            если среди типов есть временный, т.е. t, то минимум ищем по строке 
            "оценка", иначе по строке функции z
            '''

            current_vars = [i for (i, e) in zip(range(len_which_str), which_str) if e != -1]
            #print(current_vars)

            current_vars_types = [type_var[i] for i in current_vars]
            #print(current_vars_types)

            # есть ли временные пременные в составлении базиса
            temporary_vars_inv = 't' in current_vars_types
            #print(temporary_vars_inv)

            # если в строке z все коэффициенты неотрицательны, значит, решение найдено
            check = [el for (i, el) in zip(range(len_which_str), new_k) if (el < 0 and type_var[i] != "t")]
            print(check)

            break


            #         if temporary_vars_inv:
            #             # строим строку "оценка"
            #
            #             # выбираем строки, соответсвующие временным переменным
            #             tmpv = []
            #             for i in current_vars:
            #                 if type_var[i-1] == "t":
            #                     tmpv.append(which_str[i])
            #
            #             mark = [-sum([new_A[j][i] for j in tmpv]) for i in range(len_which_str)]
            #
            #             #  максимум по модулю
            #             if SHOW_PROCESS: print('mark {}'.format(mark))
            #             col = mark
            #         else:
            #             if SHOW_PROCESS: print("k: {}".format(new_k))
            #             col = new_k
            #
            #         def get_col(col, array):
            #             return list([row[col] for row in array])
            #
            #         min_col_index = col.index(min(col))
            #         min_col = get_col(min_col_index, new_A)
            #
            #         # если в разрешающем стоблце все элементы меньше или равны 0, то решений нет
            #         check = [el for el in min_col if el > 0]
            #         if not check:
            #             print("Решение не может быть найдено - задача не ограничена")
            #             return
            #
            #
            #         # находим разрешающую строку (делим элементы столбца свободных членов на соответсвующие им
            #         # элементы разрешающего стобца, и выберем минимум из неравных нулю элементов
            #         # элемент, соответсвующий разрешающей строке выходит из базиса
            #         inf = float('infinity')
            #         divide_or_inf = lambda a, b: a / b if b > 0 else inf
            #
            #         ratio = map(divide_or_inf, f, min_col)
            #         ratio = list(ratio)
            #         min_row_index = ratio.index(min(ratio))
            #
            #         # разрешающий элемент находится на пересечении разрешающего столбца и строки
            #         r_el = new_A[min_row_index][min_col_index]
            #
            #         # 00010000
            #
            #         # исключаем старую базисную переменную
            #         which_str[which_str.index(min_row_index)] = -1
            #         # помечаем новую переменную, как базисную
            #         which_str[min_col_index] = min_row_index
            #
            #
            #         # функции, одна делит весь массив на число, вторая умножает
            #         array_div = lambda array, divider: [el / divider for el in array]
            #         array_mul = lambda array, divider: [el * divider for el in array]
            #
            #
            #         # всю разрешающую строку делим на разрешающий элемент
            #         new_A[min_row_index] = array_div(new_A[min_row_index], el)
            #         min_row = new_A[min_row_index]
            #
            #         ################################################
            #
            #         #  0 в стобце для всех остальных элементов Gauss
            #         minus = lambda a, b: a - b
            #
            #         for i in [x for x in range(m) if x != min_row_index]:
            #             cur_el = new_A[i][min_col_index]
            #             if cur_el != 0:
            #                 new_A[i] = map(minus, new_A[i], array_mul(min_row, cur_el))
            #                 #############f[i] = f[i] - f[min_row_index] * cur_el
            #
            #         # тоже самое делаем для z строки
            #         cur_el = new_k[min_col_index]
            #         Z_ = map(minus, new_k, array_mul(min_row, cur_el))
            #         F = F - f[min_row_index] * cur_el
            #
            #         iter_number += 1
            #         # отчет по каждой итерации
            #         if SHOW_PROCESS:
            #             print(iter_number)
            #             print("r_el:", r_el)
            #             print("ratio:", ratio)
            #             print("k", new_k)
            #             print("current_vars: ", current_vars)
            #             print("current_vars_types: ", current_vars_types)
            #             print("temp_vars_types: ", current_vars)
            #
            #
            #         if iter_number == 100:
            #             print("Решение не найдено за 100 итераций")
            #             break
            #
            #     to_float = lambda a: [float(f) for f in a]
            #     to_float1 = lambda a: [to_float(f) for f in a]


                # check = False
            # temporary_vars_inv = False
            # if not check and not temporary_vars_inv:
            #     print('Решение найдено:')
            #
            #     # в первоначально базисных - ответ
            #     for (i, e) in enumerate(which_str):
            #         print(i, e)
            #     # print
            #     # "\n".join(["x_%d = %.4f" % (i, B[e]) for (i, e) in elements])
            #     # print
            #     #
            #     print("значение целевой функции - {}".format(F))
            #
            #     return



if __name__ == "__main__":
    print("\n", "=" * 100, "\n")

    k = [4, 6]

    # выведение функции
    print('function: \n\t max(', end=' ')

    j = 1
    for el in k:
        print('{} * x{} '.format(k[j - 1], j), end='')
        if j != len(k):
            print('+ ', end=' ')
        j += 1
    print(')\n')

    # system = [
    #     ([3, 4], ">=", 6),
    #     ([1, 3], "=", 3),
    #     ([2, 1], "<=", 4),
    # ]

    system = [
        ([1, 2], "<=", 12),
        ([3, 1], "<=", 14),
        ]


    # выведение системы

    print('system:')

    for el in system:
        j = 1
        for nel in el[0]:
            print('{} * x{} '.format(nel, j), end='')
            if j != len(el[0]):
                print('+ ', end=' ')
            j += 1
        print(el[1], el[2])

    # cоздание списка из кортежей коеф, списка знаков и списка своб членов
    A, I, f = zip(*system)
    symplex_method(A, f, I, k)

    print("\n", "=" * 60, "\n")
