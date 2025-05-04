import tkinter as tk
from tkinter import filedialog
from PIL import Image
import csv

def cargar_colores_csv():
    colores = {}
    try:
        with open("colores_encontrados.csv", "r", newline='') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                id_ = int(fila["ID"])
                hex_ = fila["Hex"].lstrip("#")
                rgb = tuple(int(hex_[i:i+2], 16) for i in (0, 2, 4))
                colores[id_] = rgb
    except FileNotFoundError:
        print("No se encontró el archivo colores_encontrados.csv.")
    return colores

def cargar_matriz_txt():
    root = tk.Tk()
    root.withdraw()
    ruta_txt = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not ruta_txt:
        print("No se seleccionó ningún archivo.")
        return None

    matriz = []
    with open(ruta_txt, "r") as f:
        for linea in f:
            fila = [int(x) for x in linea.strip().split(",") if x]
            matriz.append(fila)
    return matriz

def reconstruir_imagen():
    colores = cargar_colores_csv()
    if not colores:
        return

    matriz = cargar_matriz_txt()
    if matriz is None:
        return

    alto = len(matriz)
    ancho = len(matriz[0])

    img = Image.new("RGB", (ancho, alto))
    for y in range(alto):
        for x in range(ancho):
            id_color = matriz[y][x]
            color_rgb = colores.get(id_color, (0, 0, 0)) 
            img.putpixel((x, y), color_rgb)

    img.show()
    img.save("imagen_reconstruida.png")
    print("Imagen reconstruida y guardada como imagen_reconstruida.png.")

if __name__ == "__main__":
    reconstruir_imagen()
