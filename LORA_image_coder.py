import tkinter as tk
from tkinter import filedialog
from PIL import Image
import webcolors
import csv
import os

#RGB
css3_names_to_rgb = {
    name: webcolors.hex_to_rgb(hex)
    for name, hex in webcolors.CSS3_NAMES_TO_HEX.items()
}

def closest_color_name(rgb_tuple):
    try:
        return webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        min_dist = float('inf')
        closest_name = None
        for name, rgb in css3_names_to_rgb.items():
            dist = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, rgb_tuple))
            if dist < min_dist:
                min_dist = dist
                closest_name = name
        return closest_name

def cargar_colores_existentes():
    colores_existentes = {}
    max_id = -1
    if os.path.exists("colores_encontrados.csv"):
        with open("colores_encontrados.csv", "r", newline='') as archivo_csv:
            reader = csv.DictReader(archivo_csv)
            for fila in reader:
                id_ = int(fila["ID"])
                hex_ = fila["Hex"].lower()
                colores_existentes[hex_] = id_
                max_id = max(max_id, id_)
    return colores_existentes, max_id + 1  #ID

def guardar_nuevos_colores(nuevos_colores):
    if not nuevos_colores:
        return
    existe = os.path.exists("colores_encontrados.csv")
    with open("colores_encontrados.csv", "a", newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        if not existe:
            writer.writerow(["ID", "Hex", "Color Name"])
        for fila in nuevos_colores:
            writer.writerow(fila)

def cargar_imagen():
    #cargar CSV
    colores_existentes, next_id = cargar_colores_existentes()
    nuevos_colores = []

    #seleccionar imagen
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    if not ruta:
        print("No se seleccionó ningún archivo.")
        return

    img = Image.open(ruta).convert("RGB")
    ancho, alto = img.size
    pixeles = list(img.getdata())

    #matriz de ID
    matriz_ids = []
    for i in range(alto):
        fila = []
        for j in range(ancho):
            rgb = pixeles[i * ancho + j]
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb).lower()

            if hex_color not in colores_existentes:
                nombre_color = closest_color_name(rgb)
                colores_existentes[hex_color] = next_id
                nuevos_colores.append([next_id, hex_color, nombre_color])
                print(f"Nuevo color encontrado: {hex_color} → ID {next_id} ({nombre_color})")
                next_id += 1
            fila.append(colores_existentes[hex_color])
        matriz_ids.append(fila)

    #nuevos colores
    guardar_nuevos_colores(nuevos_colores)

    print("Todos los colores fueron procesados.")
    print(f"Imagen convertida en matriz de tamaño {alto}x{ancho} con IDs.")

    # (Opcional) guardar la matriz como archivo .txt
    with open("imagen_codificada.txt", "w") as f:
        for fila in matriz_ids:
            f.write(','.join(map(str, fila)) + '\n')
    print("Matriz de IDs guardada en imagen_codificada.txt.")

if __name__ == "__main__":
    cargar_imagen()
