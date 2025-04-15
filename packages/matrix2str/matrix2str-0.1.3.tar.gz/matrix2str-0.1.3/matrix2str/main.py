import numpy as np

def matrix2str(matrix: np.ndarray, content: str = None, precision: int = 3) -> str:
    """
    Hàm chuyển ma trận thành chuỗi
    ------------------------------
    - Bọc [ ] xung quanh ma trận
    - Điều chỉnh số chữ số thập phân
    - Căn chỉnh ma trận với nội dung đầu vào

    Các tham số:
    ------------
    `matrix`: `numpy.ndarray`, mảng 1D hoặc 2D  
    `content`: `str`, *mặc định = None*, nội dung sẽ được thêm vào ở dòng đầu tiên của ma trận  
    `precision`: `int`, *mặc định = 3*, số chữ số thập phân  

    Trả về:
    -------
    `str`  
        Chuỗi đã được bọc [ ] xung quanh, đã được điều chỉnh số chữ số thập phân, và đã được căn chỉnh với nội dung đầu vào  
    """

    precheck = len(np.array2string(matrix, max_line_width=np.inf).replace("[","").replace("]","").split("\n"))
    def getelement(x):
        rounded = f"{x:.{precision}f}"
        science = f"{x:.{precision}e}"
        return rounded if rounded != f"0.{"0"*precision}" or x == 0 else science
    longestelement = max(len(getelement(x)) for x in matrix.flatten())
    def alignelement(x):
        return getelement(x).rjust(longestelement) if precheck != 1 else getelement(x)
    matrix = np.array2string(matrix, formatter={'all':alignelement}, max_line_width=np.inf)
    matrix = matrix.replace("[","").replace("]","").split("\n")

    wrap = [""] * len(matrix)
    indent = len(content) * " "
    maxrowlen = max(len(row.strip()) for row in matrix)
    for i,row in enumerate(matrix):
        row = " " * (maxrowlen - len(row.strip())) + row.strip()
        if row.strip() == "...": row = (len(matrix[1])-5)//2 * " " + "..." + (len(matrix[1])-3)//2 * " "
        if i == 0:
            wrap[i] = f"{content}┌ {row} ┐"
        elif i == len(matrix)-1:
            wrap[i] = f"{indent}└ {row} ┘"
        else:
            wrap[i] = f"{indent}│ {row} │"

    formatted = "\n".join(wrap)
    if len(matrix) == 1: return formatted.replace("┌","[").replace("┐","]")
    else: return formatted
