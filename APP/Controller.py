import csv
import config as cf
import Model
def load_data(size):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    archivo = cf.data_dir +"BA-Grey-Wolf-tracks-utf8-" +size+".csv"
    lines_file = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    string=""
    for i in lines_file:
        string=Model.createstring(i)