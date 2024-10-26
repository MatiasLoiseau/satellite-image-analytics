import cv2
import numpy as np

# Ruta de la imagen
image_path = 'bariloche2/B1.tif'

# Cargar la imagen
image = cv2.imread(image_path)

# Verificar si la imagen es en escala de grises o color
is_gray = len(image.shape) == 2

# Variables globales para almacenar el punto inicial y final de la selección
ref_point = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping

    # Iniciar el área de selección con el primer clic
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    # Marcar el segundo punto cuando se suelta el botón izquierdo del ratón
    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False

        # Dibujar el rectángulo en la imagen
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

# Clonar la imagen para restaurarla después de dibujar
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# Mostrar la imagen y esperar hasta que se pulse la tecla 'q'
while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # Pulsar 'r' para reiniciar la selección
    if key == ord("r"):
        image = clone.copy()

    # Pulsar 'q' para salir
    elif key == ord("q"):
        break

# Si se seleccionó una región, calcular la cantidad de píxeles y el promedio de intensidad
if len(ref_point) == 2:
    roi = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
    num_pixels = roi.size if is_gray else roi.shape[0] * roi.shape[1]

    # Calcular el promedio de nivel de gris o color
    if is_gray:
        average_intensity = np.mean(roi)
        print(f"Cantidad de píxeles en la región seleccionada: {num_pixels}")
        print(f"Promedio de nivel de gris en la región seleccionada: {average_intensity:.2f}")
    else:
        mean_color = cv2.mean(roi)[:3]
        print(f"Cantidad de píxeles en la región seleccionada: {num_pixels}")
        print(f"Promedio de color en la región seleccionada: B={mean_color[0]:.2f}, G={mean_color[1]:.2f}, R={mean_color[2]:.2f}")

# Cerrar las ventanas de OpenCV
cv2.destroyAllWindows()
