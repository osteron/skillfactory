# Напишите программу, которой на вход подается последовательность чисел через пробел, а также запрашивается
# у пользователя любое число.
# В качестве задания повышенного уровня сложности можете выполнить проверку соответствия указанному в условии
# ввода данных.
# Далее программа работает по следующему алгоритму:
# Преобразование введённой последовательности в список
# Сортировка списка по возрастанию элементов в нем (для реализации сортировки определите функцию)
# Устанавливается номер позиции элемента, который меньше введенного пользователем числа, а следующий за ним больше
# или равен этому числу.
#
# При установке позиции элемента воспользуйтесь алгоритмом двоичного поиска, который был рассмотрен в этом модуле.
# Реализуйте его также отдельной функцией.
#
# Подсказка
#
# Помните, что у вас есть числа, которые могут не соответствовать заданному условию.
# В этом случае необходимо вывести соответствующее сообщение


# функция сортировки
def sorting(array):
    for i in range(1, len(array)):
        x = array[i]
        idx = i
        while idx > 0 and array[idx - 1] > x:
            array[idx] = array[idx - 1]
            idx -= 1
        array[idx] = x
    print(f'Ваши числа отсортированы по возрастанию:\n{array}\n')


# функция аварийного завершения программы
def quit_program(message):
    print(message)
    print('Выход из программы.')
    exit()


# функция двоичного поиска
def search(array, number, left, right):
    if left > right:  # если левая граница превысила правую,
        return False
    # находим середину списка
    middle = (right + left) // 2
    # сравниваем искомое число с средним и прошлым за ним
    if array[middle] >= number > array[middle - 1]:
        before, after = middle - 1, middle
        return before, after
    elif number < array[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return search(array, number, left, middle - 1)
    else:  # иначе в правой
        return search(array, number, middle + 1, right)

def main():
    # ввод набора чисел и проверка на правильность ввода
    try:
        entry = input('Введите числа через пробел (не меньше 2-х):\n')
        numbers = list(map(int, entry.split(' ')))
        entry_number = int(input('Введите искомое число:\n'))
        if len(numbers) < 2:
            quit_program('Количество чисел меньше 2.')
    except ValueError:
        quit_program('Вы ввели недопустимые символы.')
    else:
        print("Последовательность чисел принята.")

    # удаление ненужной переменной
    del entry

    # сортировка списка
    sorting(numbers)

    # переменные "до" и "после"
    before, after = None, None
    # входит ли число в диапазон списка
    if numbers[0] <= entry_number <= numbers[-1]:
        # является ли число равным первому либо последнему в списке
        if numbers[0] == entry_number or numbers[-1] == entry_number:
            quit_program("Нет чисел 'меньше' и 'больше/равно' одновременно для заданного числа.")
        # вызов функции двоичного поиска
        before, after = search(numbers, entry_number, 0, (len(numbers) - 1))
    else:
        quit_program('Число не входит в заданный диапазон.')
    # выводим позиции элементов в удобном виде (от 1 и тд)
    print(f'Число {entry_number}. Меньше: число {numbers[before]} - позиция {before + 1}, больше/равно: '
          f'число {numbers[after]} - позиция {after + 1}.')
    input("\nНажмите Enter, чтобы выйти.")

main()
