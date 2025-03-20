# generate_pdf.py


import os

# Данные для таблицы
from hw2.generator_la.generator_latex.gen_latext import generate_latex_table, generate_latex_image

data = [
    ["Header 1", "Header 2", "Header 3"],
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Генерация LaTeX кода
table = generate_latex_table(data)
image = generate_latex_image(r"C:\Users\User\Desktop\hw\python_project\pp\hw2\helper\img.png")

# Создание полного LaTeX документа
latex_document = f"""
\\documentclass{{article}}
\\usepackage{{graphicx}}
\\begin{{document}}

\\section{{Table}}
{table}

\\section{{Image}}
{image}

\\end{{document}}
"""

# Сохранение в .tex файл
with open("artifacts/before_pdf_output.tex", "w", encoding="utf-8") as f:
    f.write(latex_document)

# # Генерация PDF
# os.system("pdflatex output.tex")
#
# print("PDF успешно сгенерирован: output.pdf")