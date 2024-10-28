import cv2
import numpy as np

# Carga de la imagen multibanda
image_path = 'bariloche2/B1.tif'
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Verificamos si la imagen se cargó correctamente
if image is None:
    print("Error: No se pudo cargar la imagen.")
    exit()

# Variables globales para almacenar la selección de ROI
roi_selected = []
roi = None

# Función para dibujar la región y calcular estadísticas
def calculate_roi_statistics(event, x, y, flags, param):
    global image, roi_selected, roi

    if event == cv2.EVENT_LBUTTONDOWN:
        # Definir la esquina inicial de la región de interés
        roi_selected = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        # Definir la esquina final de la región de interés
        roi_selected.append((x, y))

        # Asegurarse de que se seleccionó un área válida
        x_start, y_start = roi_selected[0]
        x_end, y_end = roi_selected[1]

        # Asegurarse de que las coordenadas estén en orden correcto
        x_start, x_end = min(x_start, x_end), max(x_start, x_end)
        y_start, y_end = min(y_start, y_end), max(y_start, y_end)

        # Extraer la sub-imagen dentro de la ROI
        roi = image[y_start:y_end, x_start:x_end]

        # Verificar que la ROI tenga contenido válido
        if roi.size == 0:
            print("Error: La región seleccionada es inválida.")
            return

        # Mostrar la región seleccionada en la imagen original
        cv2.rectangle(image_display, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("Imagen con ROI", image_display)

        # Calcular estadísticas
        num_pixels = roi.shape[0] * roi.shape[1]
        num_bands = roi.shape[2] if len(roi.shape) == 3 else 1
        mean_per_band = np.mean(roi, axis=(0, 1)) if len(roi.shape) == 3 else [np.mean(roi)]

        # Mostrar resultados
        print(f"Cantidad de píxeles en la ROI: {num_pixels}")
        print(f"Cantidad de bandas: {num_bands}")
        print("Promedio por banda dentro de la ROI:")
        for i, mean in enumerate(mean_per_band, start=1):
            print(f"Banda {i}: {mean}")

# Crear una copia para mostrar la imagen y seleccionar la ROI
image_display = image.copy()
cv2.namedWindow("Imagen con ROI")
cv2.setMouseCallback("Imagen con ROI", calculate_roi_statistics)

print("Instrucciones: Haz clic y arrastra en la imagen para seleccionar una región.")
print("La cantidad de píxeles y el promedio de cada banda se mostrarán en la consola.")

# Mostrar la imagen y esperar a que el usuario seleccione la ROI
while True:
    cv2.imshow("Imagen con ROI", image_display)
    if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
        break

cv2.destroyAllWindows()
