import csv
import config as cf
import Model
import xlrd
import csv
import pandas as pd
def load_data(file_name):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    # open workbook by sheet index,
    # optional - sheet_by_index()
    sheet = xlrd.open_workbook("CODEFEST-2023\Documents\""+file_name).sheet_by_index(0)

    # writer object is created
    col = csv.writer(open("T.csv",
                        'w',
                        newline=""))

    # writing the data into csv file
    for row in range(sheet.nrows):
        # row by row write
        # operation is perform
        col.writerow(sheet.row_values(row))

    # read csv file and convert
    # into a dataframe object
    df = pd.DataFrame(pd.read_csv("T.csv"))

    # show the dataframe
    df

    return df

    "descartar"