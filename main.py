import numpy as np
from functions.regresion_helper import ejecutar_regresion


def main():
    # Arreglos de prueba
    x_arr = np.array([
        21.4, 10.5, 21.5, 15.6, 26.0, 20.3, 17.4, 11.3, 29.5, 19.2,
        18.2, 18.1, 28.8, 15.1, 12.0, 13.6, 22.9, 25.5, 16.6, 16.0,
        23.4, 18.1, 10.0, 28.3, 24.7, 22.5, 20.0, 25.8, 14.7, 26.3
    ])

    y_arr = np.array([
        0.8, 5.0, 1.0, 2.0, 3.1, 0.0, 1.0, 4.5, 4.5, 0.3,
        1.4, 1.2, 4.1, 2.4, 4.0, 3.4, 1.3, 2.7, 1.7, 2.0,
        1.5, 1.0, 5.2, 4.1, 2.0, 1.0, 0.0, 2.8, 2.8, 3.1
    ])

    # Variables de prueba
    var_ind = "La desviación de la temperatura ambiente respecto a la temperatura óptima"
    var_dep = "El consumo de energía diaria"
    niv_significancia = 0.05
    titulo_diagrama = "Diagrama de dispersión de el precio de un automóvil vs la cantidad de años que han transcurrido"

    # Ejecutar todo el análisis con una sola función
    regresion = ejecutar_regresion(
        x_arr,
        y_arr,
        var_ind,
        var_dep,
        niv_significancia,
        titulo_diagrama,

        # uncomment for ascii support
        #        ascii_output=True
    )


if __name__ == "__main__":
    main()
