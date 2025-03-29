import numpy as np
from functions.regresion_helper import ejecutar_regresion

def main():
    # Arreglos de prueba
    x_arr = np.array([2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14])
    y_arr = np.array([3, 5, 5.5, 6, 8, 6.8, 8.8, 9, 8.9, 9.8, 8, 10])

    # Variables de prueba
    var_ind = "la variable independiente"
    var_dep = "la variable dependiente"
    niv_significancia = 0.05
    titulo_diagrama = "Diagrama de dispersión de X vs Y"

    # Ejecutar todo el análisis con una sola función
    regresion = ejecutar_regresion(
        x_arr,
        y_arr,
        var_ind,
        var_dep,
        niv_significancia,
        titulo_diagrama,

# uncomment for ascii support
#       ascii_output=True
    )


if __name__ == "__main__":
    main()
