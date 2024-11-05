from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)  # Usar la numeración BCM
pins = [26, 19, 13, 6]

# Configurar los pines como entradas
for pin in pins:
    GPIO.setup(pin, GPIO.IN)

# Variable para almacenar los valores y tiempos
valores = []
tiempos = []

# Tiempo de inicio
inicio = time.time()

# Función para leer los valores de los pines GPIO
def leer_valores():
    while True:
        # Leer el estado de cada pin y construir un número binario
        binario = 0
        for i, pin in enumerate(pins):
            estado = GPIO.input(pin)
            # Establecer el bit correspondiente en el número binario
            binario |= (estado << i)

        # Escalar el valor binario de 0 a 5
        valor_escalado = binario  # 15 es el máximo valor en binario (1111)

        # Obtener el tiempo transcurrido desde el inicio
        tiempo_actual = time.time() - inicio
        
        # Agregar valor escalado y tiempo a las listas
        valores.append(valor_escalado)
        tiempos.append(tiempo_actual)
        
        # Limitar la lista a los últimos 60 valores
        if len(valores) > 200:
            valores.pop(0)
            tiempos.pop(0)
        
        # Esperar 1 segundo
        time.sleep(0.25)

# Iniciar el hilo de lectura de valores
threading.Thread(target=leer_valores, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/datos')
def datos():
    # Devolver los valores y tiempos en formato JSON
    return jsonify(valores=valores, tiempos=tiempos)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("Servidor detenido por el usuario.")
    finally:
        GPIO.cleanup()  # Limpiar la configuración de GPIO al finalizar

