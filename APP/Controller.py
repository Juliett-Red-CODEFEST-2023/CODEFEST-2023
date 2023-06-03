import csv
import config as cf
import Model
import xlrd
import csv
import pandas as pd
import os
import openpyxl
def load_data():
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    # open workbook by sheet index,
    # optional - sheet_by_index()
    old_name = r"C:\Users\marti\OneDrive - Universidad de los andes\Escritorio\CODEFEST-2023\Documents\NOTICIAS_DE_LA_AMAZONIA_CODEFEST.xlsx"
    
    # Read the Excel file into a DataFrame
    df = pd.read_excel(old_name)

    # Write the DataFrame to a CSV file
    df.to_csv("CSV.csv", index=False)

    # Show the DataFrame
    input_file= csv.DictReader(open("CSV.csv",encoding="utf-8"))
    for i in input_file:
        Model.ReviewData(i)

#aaaa/mm/dd