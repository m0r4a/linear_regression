import numpy as np
from scipy.stats import t
from scipy.stats import norm
from .graphic import graphic
from .table import table
from .coeficiente_correlacion import calcular_coeficiente_correlacion
from rich.console import Console
from rich.align import Align


class RegresionLineal:
    def __init__(self, x_arr, y_arr, var_ind, var_dep, niv_significancia=0.05, titulo_diagrama=None, ascii_output=False):
        """
        Inicializa el objeto de regresión lineal.

        Parámetros:
          - x_arr: Array de valores de la variable independiente.
          - y_arr: Array de valores de la variable dependiente.
          - var_ind: Descripción de la variable independiente.
          - var_dep: Descripción de la variable dependiente.
          - niv_significancia: Nivel de significancia para calcular las hipótesis.
          - titulo_diagrama: Título para el diagrama de dispersión.
        """
        self.x = np.array(x_arr)
        self.y = np.array(y_arr)
        self.ascii_output = ascii_output
        self.alpha = niv_significancia
        self.var_ind = var_ind
        self.var_dep = var_dep
        self.titulo_diagrama = titulo_diagrama or f"Diagrama de dispersión de {
            var_ind} vs {var_dep}"

        # Cantidad de datos
        self.n = len(self.x)

        # Inicializar variables de resultados
        self.resultados = {
            "correlacion": {
                "r": 0,
                "conclusion": ""
            },
            "regresion": {
                "sum_x": 0,
                "sum_y": 0,
                "mean_x": 0,
                "mean_y": 0,
                "sum_x2": 0,
                "sum_y2": 0,
                "sum_xy": 0,
                "Sxx": 0,
                "Syy": 0,
                "Sxy": 0,
                "a": 0,
                "b": 0
            },
            "determinacion": {
                "r_squared": 0,
                "SCE": 0,
                "CMT": 0,
                "CME": 0,
                "r_squared_adj": 0
            },
            "prueba_beta": {
                "error_std_b": 0,
                "ep_b": 0,
                "stat_tabla": 0,
                "stat_used": "",
                "conclusion": ""
            },
            "prueba_rho": {
                "error_std_r": 0,
                "ep_r": 0,
                "stat_tabla": 0,
                "stat_used": "",
                "conclusion": ""
            }
        }

        # Realizar todos los cálculos
        self._calcular_todo()

    def _calcular_todo(self):
        """Realiza todos los cálculos necesarios para la regresión lineal."""
        self._calcular_coeficiente_correlacion()
        self._calcular_regresion()
        self._calcular_coeficiente_determinacion()
        self._calcular_pruebas_hipotesis()

    def _calcular_coeficiente_correlacion(self):
        """Calcula el coeficiente de correlación de Pearson usando la función existente."""
        # Usar la función ya creada
        r_value, conclusion, n = calcular_coeficiente_correlacion(
            self.x, self.y, self.var_ind, self.var_dep
        )

        # Almacenar resultados
        self.resultados["correlacion"]["r"] = r_value
        self.resultados["correlacion"]["conclusion"] = conclusion

        # Calcular sumas (necesario para regresión)
        sum_x = np.sum(self.x)
        sum_y = np.sum(self.y)
        sum_xy = np.sum(self.x * self.y)
        sum_x2 = np.sum(self.x ** 2)
        sum_y2 = np.sum(self.y ** 2)

        # Guardar en resultados
        self.resultados["regresion"]["sum_x"] = round(sum_x, 4)
        self.resultados["regresion"]["sum_y"] = round(sum_y, 4)
        self.resultados["regresion"]["sum_xy"] = round(sum_xy, 4)
        self.resultados["regresion"]["sum_x2"] = round(sum_x2, 4)
        self.resultados["regresion"]["sum_y2"] = round(sum_y2, 4)

    def _calcular_regresion(self):
        """Calcula los parámetros de la regresión lineal."""
        # Calcular medias
        sum_x = self.resultados["regresion"]["sum_x"]
        sum_y = self.resultados["regresion"]["sum_y"]

        mean_x = sum_x / self.n
        mean_y = sum_y / self.n

        self.resultados["regresion"]["mean_x"] = round(mean_x, 4)
        self.resultados["regresion"]["mean_y"] = round(mean_y, 4)

        # Calcular Sxx, Syy, Sxy
        sum_x2 = self.resultados["regresion"]["sum_x2"]
        sum_y2 = self.resultados["regresion"]["sum_y2"]
        sum_xy = self.resultados["regresion"]["sum_xy"]

        Sxx = sum_x2 - self.n * mean_x ** 2
        Syy = sum_y2 - self.n * mean_y ** 2
        Sxy = sum_xy - self.n * mean_x * mean_y

        self.resultados["regresion"]["Sxx"] = round(Sxx, 4)
        self.resultados["regresion"]["Syy"] = round(Syy, 4)
        self.resultados["regresion"]["Sxy"] = round(Sxy, 4)

        # Calcular coeficientes a y b
        if Sxx == 0:
            b = 0
        else:
            b = Sxy / Sxx

        a = mean_y - b * mean_x

        self.resultados["regresion"]["b"] = b
        self.resultados["regresion"]["a"] = a

    def _calcular_coeficiente_determinacion(self):
        """Calcula el coeficiente de determinación."""
        r = self.resultados["correlacion"]["r"]
        r_squared = r ** 2
        self.resultados["determinacion"]["r_squared"] = r_squared

        # Calcular SCE (Suma de Cuadrados del Error)
        Syy = self.resultados["regresion"]["Syy"]
        SCE = Syy * (1 - r_squared)
        self.resultados["determinacion"]["SCE"] = SCE

        # Calcular CMT (Cuadrado Medio Total)
        CMT = self.resultados["regresion"]["Syy"] / (self.n - 1)
        self.resultados["determinacion"]["CMT"] = CMT

        # Calcular CME (Cuadrado Medio del Error)
        if self.n > 2:
            CME = SCE / (self.n - 2)
            self.resultados["determinacion"]["CME"] = CME

            # Calcular R² ajustado
            r_squared_adj = 1 - (CME / CMT)
            self.resultados["determinacion"]["r_squared_adj"] = r_squared_adj

    def _calcular_pruebas_hipotesis(self):
        """Calcula pruebas de hipótesis para β y ρ."""
        # Calcular el estadistico en tabla
        if self.n <= 2:
            stat_tabla = 0  # No hay grados de libertad suficientes
        elif self.n < 30:
            gl = self.n - 2
            stat_tabla = t.ppf(1 - self.alpha / 2, gl)
            stat_used = "t"
        else:
            stat_tabla = norm.ppf(1 - self.alpha / 2)
            stat_used = "z"

        self.resultados["prueba_beta"]["stat_tabla"] = stat_tabla
        self.resultados["prueba_beta"]["stat_used"] = stat_used

        self.resultados["prueba_rho"]["stat_tabla"] = stat_tabla
        self.resultados["prueba_rho"]["stat_used"] = stat_used

        # Prueba para β
        if self.resultados["determinacion"]["SCE"] > 0 and self.n > 2:
            CME = self.resultados["determinacion"]["CME"]
            Sxx = self.resultados["regresion"]["Sxx"]
            error_std_b = np.sqrt(CME / Sxx)
            self.resultados["prueba_beta"]["error_std_b"] = error_std_b

            b = self.resultados["regresion"]["b"]
            ep_b = b / error_std_b
            self.resultados["prueba_beta"]["ep_b"] = ep_b

            # Hacer la conclusión
            if ep_b < -stat_tabla:
                # Verde si se cumple
                cond1 = f"[green]{
                    round(ep_b, 4)} < -{round(stat_tabla, 4)}[/green]"
                rechazo1 = False
            else:
                # Rojo si no se cumple
                cond1 = f"[red]{
                    round(ep_b, 4)} < -{round(stat_tabla, 4)}[/red]"
                rechazo1 = True

            if ep_b > stat_tabla:
                cond2 = f"[green]{round(ep_b, 4)} > {round(
                    stat_tabla, 4)}[/green]"        # Verde si se cumple
                rechazo2 = False
            else:
                # Rojo si no se cumple
                cond2 = f"[red]{round(ep_b, 4)} > {round(stat_tabla, 4)}[/red]"
                rechazo2 = True

            if rechazo1 and rechazo2:
                conclusion_rr = ("Como se no cumple la región de rechazo entonces se rechaza Hₒ.\n"
                                 "Entonces no existe evidencia suficiente para rechazar que β = 0.\n"
                                 "Entonces no existe una relación lineal entre las variables X y Y."
                                 )
            else:
                conclusion_rr = ("Como se cumple la región de rechazo entonces se rechaza Hₒ.\n"
                                 "Entonces existe evidencia suficiente para rechazar que β = 0.\n"
                                 "Entonces existe una relación lineal entre las variables X y Y."
                                 )

            mensaje = (
                "Prueba de hipótesis de dos colas:\n"
                # "t < -t_α/2, n - 2 ó t > t_α/2, n - 2\n"
                "Se evaluó: " + cond1 + " ó " + cond2 + "\n\n" +
                conclusion_rr
            )

            self.resultados["prueba_beta"]["conclusion"] = mensaje

        # Prueba para ρ
        r = self.resultados["correlacion"]["r"]
        if self.n > 2:
            error_std_r = np.sqrt((1 - r**2) / (self.n - 2))
            self.resultados["prueba_rho"]["error_std_r"] = error_std_r

            ep_r = r / error_std_r
            self.resultados["prueba_rho"]["ep_r"] = ep_r

            # Hacer la conclusión
            if ep_r < -stat_tabla:
                # Verde si se cumple
                cond1 = f"[green]{
                    round(ep_r, 4)} < -{round(stat_tabla, 4)}[/green]"
                rechazo1 = False
            else:
                # Rojo si no se cumple
                cond1 = f"[red]{
                    round(ep_r, 4)} < -{round(stat_tabla, 4)}[/red]"
                rechazo1 = True

            if ep_r > stat_tabla:
                cond2 = f"[green]{round(ep_r, 4)} > {round(
                    stat_tabla, 4)}[/green]"        # Verde si se cumple
                rechazo2 = False
            else:
                # Rojo si no se cumple
                cond2 = f"[red]{round(ep_r, 4)} > {round(stat_tabla, 4)}[/red]"
                rechazo2 = True

            if rechazo1 and rechazo2:
                conclusion_rr = ("Como se no cumple la región de rechazo entonces no se rechaza Hₒ.\n"
                                 "Entonces no existe evidencia suficiente para rechazar que ρ = 0.\n"
                                 "Entonces no existe una correlación lineal entre las variables X y Y."
                                 )
            else:
                conclusion_rr = ("Como se cumple la región de rechazo entonces se rechaza Hₒ.\n"
                                 "Entonces existe evidencia suficiente para rechazar que ρ = 0.\n"
                                 "Entonces existe una correlación lineal entre las variables X y Y."
                                 )

            mensaje = (
                "Prueba de hipótesis de dos colas:\n"
                # "t < -t_α/2, n - 2 ó t > t_α/2, n - 2\n"
                "Se evaluó: " + cond1 + " ó " + cond2 + "\n\n" +
                conclusion_rr
            )

            self.resultados["prueba_rho"]["conclusion"] = mensaje

    def mostrar_resultados(self):
        """Muestra todos los resultados calculados en tablas."""
        # Llamar a la función table con los resultados
        table(
            self.var_ind,
            self.var_dep,
            self.resultados["correlacion"]["r"],
            self.resultados["correlacion"]["conclusion"],
            self.n,
            self.resultados
        )

    def mostrar_grafico(self, save_path="~/diagrama_dispersion.png"):
        """Muestra el gráfico de dispersión con la línea de regresión."""
        a = self.resultados["regresion"]["a"]
        b = self.resultados["regresion"]["b"]

        # Usar la función graphic actualizada para incluir la línea de regresión
        graphic(
            self.x,
            self.y,
            self.var_ind,
            self.var_dep,
            self.titulo_diagrama,
            color="mediumslateblue",
            save_path=save_path,
            a=a,
            b=b,
            ascii_output=self.ascii_output
        )

    def obtener_ecuacion_recta(self):
        """Retorna la ecuación de la recta de regresión."""
        a = self.resultados["regresion"]["a"]
        b = self.resultados["regresion"]["b"]

        if b >= 0:
            return f"ŷ = {a:.4f} + {b:.4f}x"
        else:
            return f"ŷ = {a:.4f} - {abs(b):.4f}x"

    def creditos(self):
        """Imprime en la terminal los créditos"""
        console = Console()
        console.print(Align("\nHecho por Gael Mora   ", align="right"))
