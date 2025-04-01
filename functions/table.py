from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich import box

def table(var_ind, var_dep, r_value, conclusion, n, resultados=None) -> None:
    """
    Crea y muestra una tabla completa con los resultados de la regresión lineal.

    Parámetros:
      - var_ind: variable independiente.
      - var_dep: variable dependiente.
      - r_value: String que representa el valor de r o segunda fila.
      - conclusion: Conclusión del problema.
      - n: Número de observaciones.
      - resultados: Diccionario con todos los resultados calculados (opcional).
    """
    if type(r_value) != str or type(conclusion) != str:
        r_value, conclusion = map(str, (r_value, conclusion))

    console = Console()

    # Primera tabla: Declaración de variables
    table = Table(title="Declaración de variables", box=box.ROUNDED, show_header=False)
    table.add_row("Sea x " + var_ind + " (variable independiente)\n    y " + var_dep + " (variable dependiente)")
    table.add_section()
    table.add_row("(Justificación de la relación de las variables)")
    console.print(Align(table, align="center"))

    print()

    # Segunda tabla: Diagrama de dispersión (referencia)
    table = Table(title="(Aquí va el diagrama de dispersión)", box=box.ROUNDED, show_header=False)
    table.add_row("Se guarda por defecto en ./diagrama_dispersión.png")
    table.add_section()
    table.add_row("(Lectura del diagrama)")
    console.print(Align(table, align="center"))

    print()

    # Tercera tabla: Correlación
    table = Table(title="Correlación de las variables", show_header=False, box=box.ROUNDED, style="white")
    table.add_row(f"r = {round(float(r_value), 4)}")
    table.add_section()
    table.add_row(conclusion)
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto para los cálculos
    sum_x = sum_y = mean_x = mean_y = sum_x2 = sum_y2 = sum_xy = Sxx = Syy = Sxy = 0

    # Si se proporcionan resultados, usarlos
    if resultados:
        reg = resultados.get("regresion", {})
        sum_x = reg.get("sum_x", 0)
        sum_y = reg.get("sum_y", 0)
        mean_x = reg.get("mean_x", 0)
        mean_y = reg.get("mean_y", 0)
        sum_x2 = reg.get("sum_x2", 0)
        sum_y2 = reg.get("sum_y2", 0)
        sum_xy = reg.get("sum_xy", 0)
        Sxx = reg.get("Sxx", 0)
        Syy = reg.get("Syy", 0)
        Sxy = reg.get("Sxy", 0)

    # Cuarta tabla: Suma de cuadrados
    table = Table(title="Suma de cuadrados de regresión", show_header=False, box=box.ROUNDED, style="white")
    table.add_row(f"n = {n}")
    table.add_section()
    table.add_row(f"Σx = {sum_x}", f"x̄ = {mean_x}")
    table.add_section()
    table.add_row(f"Σy = {sum_y}", f"ȳ = {mean_y}")
    table.add_section()
    table.add_row(f"Σx² = {sum_x2}", f"Sₓₓ = {Sxx}")
    table.add_section()
    table.add_row(f"Σy² = {sum_y2}", f"Sᵧᵧ = {Syy}")
    table.add_section()
    table.add_row(f"Σxy = {sum_xy}", f"Sₓᵧ = {Sxy}")
    table.add_section()
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto
    a = b = 0

    # Si se proporcionan resultados, usar valores calculados
    if resultados:
        reg = resultados.get("regresion", {})
        b = reg.get("b", 0)
        a = reg.get("a", 0)

    # Quinta tabla: Estimadores
    console.print(Align("Estimadores de mínimos cuadrados de α y β", align="center"))
    table = Table(show_header=False, box=box.ROUNDED, style="white")
    table.add_row(f"b = {b:.4f}")
    table.add_section()
    table.add_row(f"a = {a:.4f}")
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto
    r_squared = 0

    # Si se proporcionan resultados, usar valores calculados
    if resultados:
        det = resultados.get("determinacion", {})
        r_squared = det.get("r_squared", 0)

    # Sexta tabla: Coeficiente de determinación
    console.print(Align("Coeficiente de determinación", align="center"))
    table = Table(show_header=False, box=box.ROUNDED, style="white")
    table.add_row(f"r² = {r_squared:.4f} = {r_squared * 100:.2f}%")
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto
    SCE = CMT = CME = r_squared_adj = 0

    # Si se proporcionan resultados, usar valores calculados
    if resultados:
        det = resultados.get("determinacion", {})
        SCE = det.get("SCE", 0)
        CMT = det.get("CMT", 0)
        CME = det.get("CME", 0)
        r_squared_adj = det.get("r_squared_adj", 0)

    # Séptima tabla: Coeficiente de determinación ajustado
    console.print(Align("Coeficiente de determinación ajustado R²ₐⱼ", align="center"))
    table = Table(show_header=False, box=box.ROUNDED, style="white")
    table.add_row(f"SCE = {SCE:.4f}")
    table.add_section()
    table.add_row(f"CMT = {CMT:.4f}")
    table.add_section()
    table.add_row(f"CME = {CME:.4f}")
    table.add_section()
    table.add_row(f"R²ₐⱼ = {r_squared_adj:.4f} = {r_squared_adj * 100:.2f}%")
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto para prueba beta
    error_std_b = ep_b = stat_tabla = 0
    concl_beta = "(poner una variable de conclusion de hipotesis b)"

    # Si se proporcionan resultados, usar valores calculados
    if resultados:
        p_beta = resultados.get("prueba_beta", {})
        error_std_b = p_beta.get("error_std_b", 0)
        ep_b = p_beta.get("ep_b", 0)
        stat_used = p_beta.get("stat_used")
        stat_tabla = p_beta.get("t_stat_tabla", 0)
        concl_beta = p_beta.get("conclusion", concl_beta)

    # Octava tabla: Pruebas para beta
    table = Table(title="Pruebas para β", show_header=False, box=box.ROUNDED, style="white")
    table.add_row("Hₒ: β = 0")
    table.add_row("Hₐ: β ≠ 0")
    table.add_section()
    table.add_row("Error estándar del coeficiente de correlación")
    table.add_row(f"δ_b = {error_std_b:.4f}")
    table.add_section()
    table.add_row("Estadístico de prueba")
    table.add_row(f"{stat_used} = {ep_b:.4f}")
    table.add_section()
    table.add_row("Valor de tabla")
    table.add_row(f"{stat_used}_α/2, n - 2 = +- {stat_tabla:.4f}")
    table.add_section()
    table.add_row(concl_beta)
    console.print(Align(table, align="center"))

    print()

    # Valores por defecto para prueba rho
    error_std_r = ep_r = stat_tabla = 0
    concl_rho = "(poner una variable de conclusion de hipotesis p)"
    
    # Si se proporcionan resultados, usar valores calculados
    if resultados:
        p_rho = resultados.get("prueba_rho", {})
        error_std_r = p_rho.get("error_std_r", 0)
        ep_r = p_rho.get("ep_r", 0)
        stat_used = p_rho.get("stat_used")
        stat_tabla = p_rho.get("t_stat_tabla", 0)
        concl_rho = p_rho.get("conclusion", concl_rho)

    # Novena tabla: Pruebas para rho
    table = Table(title="Pruebas para ρ", show_header=False, box=box.ROUNDED, style="white")
    table.add_row("Hₒ: ρ = 0")
    table.add_row("Hₐ: ρ ≠ 0")
    table.add_section()
    table.add_row("Error estándar del coeficiente de correlación")
    table.add_row(f"δᵣ = {error_std_r:.4f}")
    table.add_section()
    table.add_row("Estadístico de prueba")
    table.add_row(f"{stat_used} = {ep_r:.4f}")
    table.add_section()
    table.add_row("Valor de tabla")
    table.add_row(f"{stat_used}_α/2, n - 2 = +- {stat_tabla:.4f}")
    table.add_section()
    table.add_row(concl_rho)
    console.print(Align(table, align="center"))

