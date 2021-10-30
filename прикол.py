new_tramway_line = {"Писарева": (1, 0),
                    "1000 мелочей": (2, 5),
                    "Стадион Спартак": (3, 7),
                    "Театр Оперы и балета": (4, 5),
                    "Депутатская": (5, 12),
                    "Октябрьская": (6, 3),
                    "Фабрика ШК Швейников": (7, 7),
                    "Мостовая": (8, 8),
                    "Маяковского": (9, 2)}

start = input("Введите начальную остановку: ")
end = input("Введите конечную остановку: ")
total = 0

if start and end in new_tramway_line.keys():
    begin_cicle = new_tramway_line[start][0] + 1
    end_cicle = new_tramway_line[end][0]

    if new_tramway_line[start][0] < new_tramway_line[end][0]:
        # Прямое направление
        for i in range(begin_cicle, end_cicle+1):
            for key, value in new_tramway_line.values():
                if i == key:
                    total += value
    else:
        # Обратное направление
        for i in range(end_cicle, begin_cicle):
            for key, value in new_tramway_line.values():
                if i == key:
                    total += value
    print(f"Итоговое время в пути = {total}")
else:
    print("Таких остановок нет, либо Вы ввели их неправильно.")
