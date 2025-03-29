from .regresion_lineal import RegresionLineal

def ejecutar_regresion(x_arr, y_arr, var_ind, var_dep, niv_significancia=0.05, titulo_diagrama=None, save_path="./diagrama_dispersion.png"):
    """
    Función auxiliar para ejecutar todo el proceso de regresión lineal de manera sencilla.

    Parámetros:
      - x_arr: Array de valores de la variable independiente.
      - y_arr: Array de valores de la variable dependiente.
      - var_ind: Descripción de la variable independiente.
      - var_dep: Descripción de la variable dependiente.
      - niv_significancia: Nivel de significancia para calcular las hipótesis.
      - titulo_diagrama: Título para el diagrama de dispersión.
      - save_path: Ruta donde guardar el diagrama de dispersión.

    Retorna:
      - Un objeto RegresionLineal con todos los cálculos realizados.
    """
    regresion = RegresionLineal(x_arr, y_arr, var_ind, var_dep, niv_significancia, titulo_diagrama)
    regresion.mostrar_resultados()
    regresion.mostrar_grafico(save_path=save_path)

    return regresion  # Por si el que lo use quiere un valor en particular
