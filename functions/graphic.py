import matplotlib.pyplot as plt
import numpy as np
import warnings

def show_ascii_plot(x_arr, y_arr, nombre_var_ind, nombre_var_dep, titulo_diagrama, color, a=None, b=None):
    """
    Muestra un gráfico de dispersión en la terminal usando plotext.

    Parámetros:
      - x_arr, y_arr: Datos a graficar.
      - nombre_var_ind: Nombre de la variable independiente.
      - nombre_var_dep: Nombre de la variable dependiente.
      - titulo_diagrama: Título del gráfico.
      - color: color del marker.
      - a: Intercepto de la línea de regresión (opcional).
      - b: Pendiente de la línea de regresión (opcional).
    """
    try:
        import plotext as plt_ascii
        x, y = x_arr.tolist(), y_arr.tolist()
        plt_ascii.scatter(x, y, color=color, marker='hd', label="Datos")

        # Si se proporcionan a y b, añadir línea de regresión
        if a is not None and b is not None:
            x_min, x_max = min(x), max(x)
            x_line = np.linspace(x_min, x_max, 100)
            y_line = b * x_line + a
            plt_ascii.plot(x_line.tolist(), y_line.tolist(), color="red", label=f"ŷ = {a:.2f} + {b:.2f}x")

        plt_ascii.title(titulo_diagrama)
        plt_ascii.theme("clear")
        plt_ascii.plot_size(180, 40)
        plt_ascii.xlabel(nombre_var_ind)
        plt_ascii.ylabel(nombre_var_dep)
        plt_ascii.show()
    except ImportError:
        print("Para la salida ASCII, instala plotext: pip install plotext")


def graphic(x_arr, y_arr, nombre_var_ind="Eje X", nombre_var_dep="Eje Y", titulo_diagrama="Diagrama de dispersión", color="mediumslateblue", save_path="./diagrama_dispersion.png", ascii_output=False, a=None, b=None):
    """
    Crea un diagrama de dispersión comparando dos arreglos numéricos y opcionalmente añade la línea de regresión.

    Parámetros:
      - x_arr: arreglo del eje X a graficar (var independiente).
      - y_arr: arreglo del eje Y a graficar (var dependiente).
      - nombre_var_ind: Nombre de la variable independiente.
      - nombre_var_dep: Nombre de la variable dependiente.
      - titulo_diagrama: Título del gráfico.
      - color: Color de los puntos de dispersión.
      - save_path: Ruta para guardar la imagen (ej: 'grafico.png').
      - ascii_output: Si es True, muestra la salida en ASCII.
      - a: Intercepto de la línea de regresión (opcional).
      - b: Pendiente de la línea de regresión (opcional).
    """

    # Esta List Comprehension itera sobre ambos arreglos y verifica si alguno
    # no es un numpy array; en ese caso, lo convierte.
    x_arr, y_arr = (np.array(a_val) if not isinstance(a_val, np.ndarray) else a_val for a_val in (x_arr, y_arr))
    nombre_var_ind, nombre_var_dep = (str(a_val) if not type(a_val) == str else a_val for a_val in (nombre_var_ind, nombre_var_dep))

    if ascii_output:
        show_ascii_plot(x_arr, y_arr, nombre_var_ind, nombre_var_dep, titulo_diagrama, color, a, b)
        return

    # Se fuerza el uso del estilo 'ggplot'
    plt.style.use('ggplot')

    plt.figure(figsize=(10, 5))

    # Graficar los puntos de dispersión
    plt.scatter(x_arr, y_arr, color=color, label="Datos")

    # Si se proporcionan a y b, añadir línea de regresión
    if a is not None and b is not None:
        x_min, x_max = np.min(x_arr), np.max(x_arr)
        x_line = np.linspace(x_min, x_max, 100)
        y_line = b * x_line + a

        # Graficar la línea de regresión en rojo
        plt.plot(x_line, y_line, color='red', linewidth=2, label=f"Línea de regresión")

        # Añadir texto con la ecuación de la línea
        # Posicionar el texto en la parte superior izquierda
        text_x = x_min + 0.05 * (x_max - x_min)
        text_y = np.max(y_arr) - 0.1 * (np.max(y_arr) - np.min(y_arr))

        # Determinar si la pendiente es positiva o negativa para formatear correctamente
        if b >= 0:
            equation_text = f"ŷ = {a:.3f} + {b:.3f}x"
        else:
            equation_text = f"ŷ = {a:.3f} - {abs(b):.3f}x"

        plt.text(text_x, text_y, equation_text, fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='darkgray'))

    plt.title(titulo_diagrama)
    plt.xlabel(nombre_var_ind)
    plt.ylabel(nombre_var_dep)
    plt.grid(True)
    plt.legend()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("error", category=UserWarning)
                plt.show()
        except UserWarning as e:
            print(f"Error al mostrar el gráfico con Matplotlib: {e}\nIntenando salida ASCII...")
            show_ascii_plot(x_arr, y_arr, nombre_var_ind, nombre_var_dep, titulo_diagrama, color, a, b)
