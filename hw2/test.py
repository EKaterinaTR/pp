from hw2.table_latext import generate_latex_table


def save_table(data, name_file):
    # Генерация LaTeX кода для таблицы
    latex_code = generate_latex_table(data)

    # Сохранение результата в .tex файл
    with open(f"artifacts/{name_file}.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)


data = {
    'test_1': [
        ["Header 1", "Header 2", "Header 3"],
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    'test_2': [
        ["Header 1", "Header 2", "Header 3", "Header 4"],
        ['1', '2', '3', '4'],
        ['a', 'b', 'c', 'd'],
    ],
    'test_3': [
        ["Header 1", "Header 2", "Header 3", "Header 4"],
        [1.2, 2.3, 5.6, 8.8]
    ]
}
for k in data:
    save_table(data[k], k)
