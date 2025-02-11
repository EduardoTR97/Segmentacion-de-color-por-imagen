import cv2
import numpy as np
import time  # Importar time para usar el temporizador


# Definir los rangos HSV para azul, verde y rojo
lower_blue = np.array([70, 160, 40])  # Ajusta estos valores según tus pruebas
upper_blue = np.array([140, 255, 255])

lower_green = np.array([30, 45, 40])   # Ajusta estos valores según tus pruebas
upper_green = np.array([80, 255, 255])

# Rangos para rojo (dividido en dos partes)
lower_red1 = np.array([0, 120, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 50])
upper_red2 = np.array([180, 255, 255])

# Definir los puntos del rectángulo delimitador
p1 = (80, 20)
p2 = (200, 20)
p3 = (200, 230)
p4 = (80, 230)

#lista generales de colores 
objetosrojos=[]
objetosazules=[]
objetosverdes=[]
resultados=[]

# Crear el arreglo de puntos para el polígono
rectangle_points = np.array([p1, p2, p3, p4], dtype=np.int32)

# Iniciar la captura de video utilizando DirectShow y configurar resolución
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Ancho
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Altura

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    # Leer una imagen de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen al espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear máscaras monocromáticas para azul, verde y rojo
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)  # Combinar las dos máscaras para rojo

    # Aplicar operaciones morfológicas para limpiar las máscaras
    kernel = np.ones((5, 5), np.uint8)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)

    # Crear máscaras coloreadas para azul, verde y rojo
    colored_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    colored_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    colored_red = cv2.bitwise_and(frame, frame, mask=mask_red)

    # Encontrar contornos para cada color
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar el rectángulo delimitador
    cv2.polylines(frame, [rectangle_points], isClosed=True, color=(0, 255, 0), thickness=2)

    # Calcular el desplazamiento de las coordenadas (p1)
    offset_x, offset_y = p1
    count_blue = 0
    count_green = 0
    count_red = 0
    # Dibujar los centros de los contornos y rotarlos
    for contour in contours_blue:
        if cv2.contourArea(contour) > 500:  # Ignorar áreas pequeñas
            # Obtener el rectángulo mínimo alrededor del contorno
            count_blue += 1
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            # Verificar si el centro del contorno está dentro del área delimitada
            center = (int(rect[0][0]), int(rect[0][1]))
            if cv2.pointPolygonTest(rectangle_points, center, False) >= 0:
                # Calcular el ángulo de rotación
                angle = rect[2]
                # Mostrar el ángulo de rotación
                cv2.putText(frame, f"Angle: {angle:.2f}", (center[0] - 20, center[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                # Restar el desplazamiento (offset) para redefinir las coordenadas dentro del rectángulo
                center_offset = (center[0] - offset_x, center[1] - offset_y)
                # Dibujar el centro como un punto
                cv2.circle(frame, center, 5, (255, 0, 0), -1)
                cv2.putText(frame, "Blue", (center[0] - 20, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                cv2.putText(frame, f"({center_offset[0]}, {center_offset[1]})", (center[0] - 20, center[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                # Dibujar el rectángulo rotado
                cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)
                text_position = (10, 20)  # Posición inicial del texto
                cv2.putText(frame, f"Blue: {count_blue}", (text_position[0], text_position[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                objetosazules.append(["Azul",center_offset[0],center_offset[1],angle])
    
                


    for contour in contours_green:
        if cv2.contourArea(contour) > 500:  # Ignorar áreas pequeñas
            count_green += 1
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            center = (int(rect[0][0]), int(rect[0][1]))
            if cv2.pointPolygonTest(rectangle_points, center, False) >= 0:
                angle = rect[2]
                cv2.putText(frame, f"Angle: {angle:.2f}", (center[0] - 20, center[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                center_offset = (center[0] - offset_x, center[1] - offset_y)
                cv2.circle(frame, center, 5, (0, 255, 0), -1)
                cv2.putText(frame, "Green", (center[0] - 20, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"({center_offset[0]}, {center_offset[1]})", (center[0] - 20, center[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                text_position = (10, 20)  # Posición inicial del texto
                cv2.putText(frame, f"Green: {count_green}", (text_position[0], text_position[1] + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                objetosverdes.append(["Verde",center_offset[0],center_offset[1],angle])
    

    for contour in contours_red:
        if cv2.contourArea(contour) > 500:  # Ignorar áreas pequeñas
            count_red += 1
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            center = (int(rect[0][0]), int(rect[0][1]))
            if cv2.pointPolygonTest(rectangle_points, center, False) >= 0:
                angle = rect[2]
                cv2.putText(frame, f"Angle: {angle:.2f}", (center[0] - 20, center[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                center_offset = (center[0] - offset_x, center[1] - offset_y)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                cv2.putText(frame, "Red", (center[0] - 20, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.putText(frame, f"({center_offset[0]}, {center_offset[1]})", (center[0] - 20, center[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                text_position = (10, 20)  # Posición inicial del texto
                cv2.putText(frame, f"Red: {count_red}", (text_position[0], text_position[1] + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                objetosrojos.append(["Rojo",center_offset[0],center_offset[1],angle])

    # Combinar las máscaras coloreadas para una vista combinada
    combined_colored_masks = cv2.addWeighted(
        cv2.addWeighted(colored_blue, 1, colored_green, 1, 0), 1, colored_red, 1, 0
    )

    # Mostrar las máscaras y la imagen principal con detecciones
    cv2.imshow("Mask Blue (Monochrome)", mask_blue)       # Máscara monocromática azul
    cv2.imshow("Mask Green (Monochrome)", mask_green)     # Máscara monocromática verde
    cv2.imshow("Mask Red (Monochrome)", mask_red)         # Máscara monocromática roja
    cv2.imshow("Colored Blue Mask", colored_blue)         # Máscara azul coloreada
    cv2.imshow("Colored Green Mask", colored_green)       # Máscara verde coloreada
    cv2.imshow("Colored Red Mask", colored_red)           # Máscara roja coloreada
    cv2.imshow("Detected Colors (Main Frame)", frame)     # Imagen principal con detecciones
    cv2.imshow("Combined Colored Masks", combined_colored_masks)  # Máscaras combinadas

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print(objetosrojos)
print(objetosverdes)
print(objetosazules)
print(count_blue)
for i in range(count_blue):
    resultados.append(objetosazules[-count_blue])
for i in range(count_red):
    resultados.append(objetosrojos[-count_red])
for i in range(count_green):
    resultados.append(objetosverdes[-count_green])
print(resultados)

