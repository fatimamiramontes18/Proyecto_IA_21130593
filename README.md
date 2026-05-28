Control de Acceso Biométrico para Mascotas con IA e IoT
Materia:Inteligencia Artificial  
Autor:Fátima Sahori De La Paz Miramontes  
Institución:Instituto Tecnológico de La Laguna  

Este repositorio contiene la implementación práctica de un sistema de acceso bimodal y exclusivo para mascotas autorizadas (Arisca, SKY y Goyo), integrando redes neuronales convolucionales profundas y control de hardware local.


Arquitectura y Funcionamiento General
El sistema opera mediante un puente distribuido de software y hardware:
1. Detección de Objetos (YOLOv8):Una cámara web captura el video local y el modelo `best.pt` localiza geométricamente la silueta del animal en tiempo real.
2. Validación de Identidad Cromática (OpenCV):El sistema extrae la Región de Interés (ROI) de la imagen, la transforma al espacio de color HSV y calcula su histograma de color para validar que el pelaje corresponda exactamente a una de las mascotas registradas.
3. Control Serie e IoT (Arduino Uno):Al autenticar con éxito al animal, Python transmite el carácter binario `b'A'` mediante el puerto serie USB (9600 baudios) para activar el mecanismo físico.



Análisis del Modelo de IA y Métricas
-Eficacia Estructural:El modelo alcanzó una precisión general mAP50 del 99.5% en el conjunto de validación tras 40 épocas de optimización en una GPU Tesla T4.
-Matriz de Confusión:La diagonal principal reporta un 0.99 de éxito continuo para las clases Arisca, SKY y Goyo, demostrando una separación matemática ideal de fronteras morfológicas.
-Los registros completos del entrenamiento, curvas de pérdida (Loss) y matrices de precisión se encuentran resguardados dentro de la carpeta `/runs` de este repositorio.



Limitaciones del Sistema y Mitigación de Erreurs
Durante la etapa de pruebas, se identificó una vulnerabilidad de Sobreajuste Local / Sesgo de Fondo: la IA promediaba el entorno físico compartida y llegó a confundir el rostro de la desarrolladora con la clase `Goyo` al 67.4% de certeza.

Mecanismos de Blindaje Implementados en Código:
1. Filtro de String Matching Estricto:Se restringió el paso de datos en Python para ignorar IDs ajenos o clases genéricas de fábrica del modelo YOLO base.
2. Candado de Confianza Dinámica al 90%:Al identificar el falso positivo humano a un techo del 67.4%, se elevó el umbral condicional en Python al 90% (`conf=0.90`) para la clase conflictiva. El rostro humano es rechazado permanentemente, mientras que las mascotas reales superan el umbral con facilidad.
3. Doble Factor de Autenticación (2FA Cromatico):Si se presenta un animal de la misma especie de internet, YOLO aprueba la forma, pero OpenCV evalúa el histograma del pelaje mediante correlación matemática de Pearson. Si la similitud es menor al 70%, el acceso es denegado de inmediato.


Circuito Esquemático y Aclaración de la Simulación
-NOTA DE SIMULACIÓN CRÍTICA: Al tratarse de un prototipo de laboratorio a nivel funcional, los actuadores mecánicos reales de una compuerta (solenoides o servomotores) han sido sustituidos por un símil electrónico basado en diodos LED, los cuales representan visual y lógicamente el estado actual de la puerta inteligente.

Comportamiento de los Estados de la Puerta:
LED Rojo (Pin Digital 13): Puerta Cerrada / Bloqueo Fijo: Es el estado de reposo seguro por defecto del sistema. Se mantiene activo mientras no haya mascotas autorizadas en el encuadre o se detecten falsos positivos humanos/impostores.
LED Verde (Pin Digital 12): Puerta Abierta / Acceso Concedido:Se activa de forma síncrona únicamente cuando la IA y OpenCV validan con éxito la identidad biométrica de la mascota. Permanece energizado durante un temporizador de 5000 ms (5 segundos) antes de ejecutar un vaciado de búfer serie y regresar al estado de bloqueo automático.

Conexión Física (Esquema):
-`Arduino Pin 13` ──> [Resistencia 220 Ohms] ──> [Ánodo (+) LED Rojo] ──> [Cátodo (-) Gnd]
- `Arduino Pin 12` ──> [Resistencia 220 Ohms] ──> [Ánodo (+) LED Verde] ──> [Cátodo (-) Gnd]
