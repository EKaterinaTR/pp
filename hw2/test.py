from typing import List

from hw2.generator_latex.gen_latext import generate_latex_table, create_doc_latex


def save_table(data:List, name_file:str):
    latex_code = create_doc_latex(generate_latex_table(data))
    with open(f"artifacts/{name_file}.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)


data = {
    'test_1': [
        ["Header 11", "Header 22", "Header 33"],
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
