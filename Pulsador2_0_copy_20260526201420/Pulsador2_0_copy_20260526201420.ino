// ============================================================================
// PROYECTO: PUERTA DE RECONOCIMIENTO DE MASCOTAS CON IA (YOLOv8 + PYTHON)
// AUTORA: Fátima De la Paz Miramontes
// MATERIA: Inteligencia Artificial / Proyecto Integrador
// ============================================================================

// Definición de los pines digitales asignados a los LEDs indicadores
const int pinVerde = 12; // Pin digital para el LED Verde (Acceso Autorizado)
const int pinRojo = 13;  // Pin digital para el LED Rojo (Puerta Cerrada / Bloqueada)

void setup() {
  // Inicialización del puerto serie a 9600 baudios.
  // Es la velocidad de sincronización estándar para comunicarse con el script de Python.
  Serial.begin(9600); 
  
  // Configuración de los pines como salidas de corriente (OUTPUT)
  pinMode(pinVerde, OUTPUT);
  pinMode(pinRojo, OUTPUT);
  
  // ESTADO INICIAL SEGURO: Al energizar el Arduino, la puerta inicia "CERRADA".
  // Activamos el LED Rojo (HIGH) y nos aseguramos de mantener el Verde apagado (LOW).
  digitalWrite(pinRojo, HIGH);
  digitalWrite(pinVerde, LOW);
}

void loop() {
  // Verificamos de forma constante si hay bytes de datos disponibles en el búfer serie
  if (Serial.available() > 0) {
    
    // Lectura del carácter enviado por el script de YOLOv8 a través del cable USB
    char senal = Serial.read(); 
    
    // EVALUACIÓN DE LA SEÑAL:
    // Si el carácter recibido coincide estrictamente con la 'A' (Señal de Apertura)...
    if (senal == 'A') { 
      
      // 1. MASCOTA AUTORIZADA: Conmutación de estados en los actuadores (LEDs)
      digitalWrite(pinRojo, LOW);     // Apagamos el indicador de bloqueo (Rojo)
      digitalWrite(pinVerde, HIGH);   // Encendemos el indicador de apertura (Verde)
      
      // 2. TEMPORIZACIÓN DE APERTURA:
      // Mantenemos el estado de acceso activo durante 5000 milisegundos (5 segundos).
      // Este delay físico está sincronizado con el 'time.sleep(5)' del script de Python.
      delay(5000); 
      
      // 3. RESTABLECIMIENTO DEL SISTEMA (Cierre Automático):
      // Finalizado el tiempo de cortesía, el sistema regresa a su estado seguro inicial.
      digitalWrite(pinVerde, LOW);    // Apagamos el acceso (Verde)
      digitalWrite(pinRojo, HIGH);    // Reactivamos el bloqueo fijo (Rojo)
      
      // Limpieza del búfer serie para evitar lecturas de datos basura o duplicados
      while(Serial.available() > 0) {
        Serial.read();
      }
    }
  }
}