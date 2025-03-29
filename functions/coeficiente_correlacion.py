import numpy as np
from scipy import stats

def calcular_coeficiente_correlacion(arr1, arr2, nombre_var_ind="(variable independiente)", nombre_var_dep="(variable dependiente)"):
    """
    Calcula la correlación entre dos arreglos usando el método especificado.

    Parámetros:
      - arr1, arr2: Arreglos (o listas) de datos numéricos.
      - nombre_var_ind: Es el nombre de la var. independiente declarada (solo se usa para concluir)
      - nombre_var_dep: Es el nombre de la var. dependiente declarada (solo se usa para concluir)

    Retorna:
      - Una tupla (coeficiente, conclusión).
    """

    arr1, arr2 = (np.array(a) if not isinstance(a, np.ndarray) else a for a in (arr1, arr2))

    r, _ = stats.pearsonr(arr1, arr2)

    match r:
        case _ if 0.5 < r < 1:
            conclusion = f"Como 0.5 < r < 1 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera fuerte y positiva."
        case 0.5:
            conclusion = f"Como r = 0.5 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera moderada y positiva."
        case _ if 0 < r < 0.5:
            conclusion = f"Como 0 < r < 0.5 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera débil y positiva."
        case _ if -1 < r < -0.5:
            conclusion = f"Como -1 < r < -0.5 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera fuerte y negativa."
        case -0.5:
            conclusion = f"Como r = -0.5 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera moderada y negativa."
        case _ if -0.5 < r < 0:
            conclusion = f"Como -0.5 < r < 0 entonces la correlación entre {nombre_var_dep} y el/la {nombre_var_ind} se considera débil y negativa."
        case 0:
            conclusion = f"Como r = 0 entonces la correlación es inexistente"
        case _:
            conclusion = "El valor de r no está en el rango esperado (-1, 1)."

    return (r, conclusion, len(arr1))
