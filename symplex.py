"""
    Алгортм:
        Приведение к каноническому виду:
            - для знака <=
            - для знака >=
            - для знака =
"""
import numpy


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


def symplex_method(A, F, I, k):
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
        # если переменная базисная (true), запоминаем строку
        which_str = which_str + [(cnt.inc() if letter else -1) for letter in basic]
        type_var = type_var + t_var
        add = add + arr
        i += 1

    num_add = len(add)
    # print(add)
    tr_add = numpy.transpose(add)
    # print(tr_add)

    new_A = list()
    for i in enumerate(tr_add):
        n = list(tr_add[i[0]])
        new = A[i[0]] + n
        new_A.append(new)

    # print('new_A', new_A)



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

    system = [
        ([3, 4], ">=", 6),
        ([1, 3], "=", 3),
        ([2, 1], "<=", 4),
    ]

    # выведение системы

    print('system:')

    for el in system:
        j = 1
        for nel in el[0]:
            print('{} * x{} '.format(el[0][j - 1], j), end='')
            if j != len(el[0]):
                print('+ ', end=' ')
            j += 1
        print(el[1], el[2])

    # cоздание списка из кортежей коеф, списка знаков и списка своб членов
    A, I, F = zip(*system)
    symplex_method(A, F, I, k)

    print("\n", "=" * 60, "\n")
