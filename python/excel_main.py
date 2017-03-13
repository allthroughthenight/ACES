from linear_wave_theory import *
import xlrd

#----------------------------------------------------------------------
def open_file(path):
    """
    Open and read an Excel file

    book = xlrd.open_workbook(path)

    # print number of sheets
    print book.nsheets

    # print sheet names
    print book.sheet_names()

    # get the first worksheet
    first_sheet = book.sheet_by_index(0)

    # read a row
    print first_sheet.row_values(0)

    # read a cell
    cell = first_sheet.cell(0,0)
    print cell
    print cell.value

    # read a row slice
    print first_sheet.row_slice(rowx=0,
                                start_colx=0,
                                end_colx=2)

    """
    # H, T, d, z, xL
    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0)
    cellH = first_sheet.cell(0,0).value
    cellT = first_sheet.cell(0,1).value
    celld = first_sheet.cell(0,2).value
    cellz = first_sheet.cell(0,3).value
    cellxL = first_sheet.cell(0,4).value

    temp = LinearWaveTheoryOutput()
    temp.H, temp.T, temp.d, temp.z, temp.xL, temp.L, temp.C, temp.Cg, temp.E, \
        temp.Ef, temp.Ur, temp.eta, temp.px, temp.py, temp.pz, temp.u, temp.w, \
        temp.dudt, temp.dwdt, temp.pres = \
        linearWaveTheory(cellH, cellT, celld, cellz, cellxL, 'I')
    temp.toString()

#----------------------------------------------------------------------
if __name__ == "__main__":
    path = "test.xlsx"
    open_file(path)
