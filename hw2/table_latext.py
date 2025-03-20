from functools import reduce


def generate_latex_table(data):
    if not data:
        return ""

    columns = len(data[0])

    latex_table = f"\\begin{{document}}\\begin{{tabular}}{{|{'|'.join(['c'] * columns)}|}}\n\\hline\n"


    rows = reduce(
        lambda acc, row: acc + f"{' & '.join(map(str, row))} \\\\\n\\hline\n",
        data,
        latex_table
    )

    latex_table = rows + "\\end{tabular}\\end{document}"

    return latex_table
