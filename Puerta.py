# ============================================================================
# PROYECTO: PUERTA INTELIGENTE CON BIOMETRÍA DE COLOR (ANTI-IMPOSTORES)
# AUTORA: Fátima De la Paz Miramontes
# ============================================================================

import cv2
from ultralytics import YOLO
import serial
import time
import numpy as np

puerto_arduino = 'COM5' 
try:
    arduino = serial.Serial(puerto_arduino, 9600, timeout=1)
    time.sleep(2)
    print(f"✅ Conectado al Arduino en: {puerto_arduino}")
except:
    print(f"⚠️ Funcionando en MODO SIMULACIÓN")
    arduino = None

model = YOLO("best.pt")
cap = cv2.VideoCapture(0)

# ============================================================================
# HISTOGRAMAS DE REFERENCIA (El pelaje real de tus mascotas)
# Si notas que no entran, borra estos valores para que el sistema los recalibre
# ============================================================================
hist_referencia = {
    'gato': None,
    'perro_1': None,
    'perro_2': None
}

print("\n🔒 SISTEMA BIOMÉTRICO ACTIVO. Validando identidad estricta...")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=0.65, classes=[0, 1, 2], stream=True)
    mascota_autentica = False

    for r in results:
        frame = r.plot()
        
        for box in r.boxes:
            id_real = int(box.cls[0])
            confianza_ia = float(box.conf[0])
            nombre_clase = str(model.names[id_real]).strip().lower()
            
            # Coordenadas del recorte de la mascota
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)
            
            # Extraemos la región de interés (el cuerpo del animal)
            recorte = frame[y1:y2, x1:x2]
            if recorte.size == 0:
                continue
                
            # Calculamos el histograma de color HS (Tono y Saturación) del pelaje
            hsv_recorte = cv2.cvtColor(recorte, cv2.COLOR_BGR2HSV)
            hist_actual = cv2.calcHist([hsv_recorte], [0, 1], None, [50, 60], [0, 180, 0, 256])
            cv2.normalize(hist_actual, hist_actual, 0, 1, cv2.NORM_MINMAX)
            
            # 🔄 MODO AUTOCALIBRACIÓN: Si es la primera vez que ve a tu mascota real, guarda su color
            if hist_referencia[nombre_clase] is None:
                hist_referencia[nombre_clase] = hist_actual
                print(f"📸 [CALIBRACIÓN] Pelaje de {nombre_clase} memorizado con éxito. ¡Identidad protegida!")
            
            # 🔍 COMPARACIÓN BIOMÉTRICA DE COLOR (Correlación matemática)
            similitud_color = cv2.compareHist(hist_referencia[nombre_clase], hist_actual, cv2.HISTCMP_CORREL)
            
            print(f"📊 Análisis para [{nombre_clase}]: Confianza Forma: {confianza_ia*100:.1f}% | Similitud Pelaje: {similitud_color*100:.1f}%")
            
            # FILTRO DE EXCLUSIVIDAD:
            # Debe parecerse físicamente (YOLO) Y además el color de su pelo debe coincidir en más de un 70%
            if similitud_color > 0.70:
                mascota_autentica = True
                mascota_nombre = nombre_clase
                break
            else:
                print(f"❌ [ALERTA] Forma correcta ({nombre_clase}) pero el color del pelaje NO coincide. Acceso Denegado.")

    if mascota_autentica and arduino:
        print(f"🔓 [BIOMETRÍA APROBADA] Abriendo puerta para tu verdadera mascota: {mascota_nombre}\n")
        arduino.write(b'A') 
        time.sleep(5) 

    cv2.imshow("Puerta Inteligente - Filtro Biometrico de Pelaje", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()