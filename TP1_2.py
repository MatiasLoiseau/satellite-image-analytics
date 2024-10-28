#%%
import cv2
import matplotlib.pyplot as plt
import os

# Definir la carpeta de las imágenes de entrada y salida
input_folder = 'bariloche2'
output_folder = 'output'

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Función para cargar y desplegar una imagen
def load_and_display_image(filename):
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error al cargar la imagen {filename}.")
    else:
        print(f"Imagen {filename} cargada correctamente.")
        plt.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
        plt.title(f"Display de {filename}")
        plt.axis("off")
        plt.show()
    return img

# Función para guardar una imagen en un archivo
def save_image(img, output_filename):
    cv2.imwrite(output_filename, img)
    print(f"Imagen guardada como {output_filename}")

# Función para obtener el valor de un píxel específico en una imagen
def get_pixel_value(img, x, y):
    if x < img.shape[1] and y < img.shape[0]:  # Verifica que esté dentro de los límites
        pixel_value = img[y, x]
        print(f"Valor del píxel en ({x}, {y}): {pixel_value}")
        return pixel_value
    else:
        print("Las coordenadas están fuera del límite de la imagen.")
        return None

# Función para copiar una parte de la imagen en una nueva imagen
def copy_image_section(img, x_start, y_start, width, height):
    if (x_start + width <= img.shape[1]) and (y_start + height <= img.shape[0]):
        cropped_img = img[y_start:y_start + height, x_start:x_start + width]
        print("Sección copiada exitosamente.")
        plt.imshow(cropped_img, cmap='gray' if len(cropped_img.shape) == 2 else None)
        plt.title("Imagen Copiada")
        plt.axis("off")
        plt.show()
        return cropped_img
    else:
        print("Las dimensiones están fuera del límite de la imagen.")
        return None

# Función para guardar la imagen cortada con otro nombre
def save_cropped_image(cropped_img, filename):
    if cropped_img is not None:
        cv2.imwrite(filename, cropped_img)
        print(f"Imagen cortada guardada como {filename}")
    else:
        print("No se pudo guardar la imagen cortada. Asegúrate de haberla copiado correctamente.")

# Ejemplo de uso de las funciones
if __name__ == "__main__":
    # Procesar cada imagen desde B1.tif hasta B8.tif
    for i in range(1, 9):
        input_filename = os.path.join(input_folder, f'B{i}.tif')
        output_filename = os.path.join(output_folder, f'B{i}_guardada.jpg')
        cropped_output_filename = os.path.join(output_folder, f'B{i}_cortada.jpg')

        # Cargar y desplegar la imagen
        img = load_and_display_image(input_filename)

        # Guardar la imagen cargada
        if img is not None:
            save_image(img, output_filename)

            # Obtener el valor de un píxel específico (por ejemplo, en las coordenadas (100, 50))
            get_pixel_value(img, 100, 50)

            # Copiar una sección de la imagen (por ejemplo, desde (50, 50) con tamaño 100x100)
            cropped_img = copy_image_section(img, 50, 50, 100, 100)

            # Guardar la imagen cortada
            save_cropped_image(cropped_img, cropped_output_filename)

#%%
