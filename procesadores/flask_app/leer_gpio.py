import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)  # Usar la numeración BCM
pins = [26, 19, 13, 6]

# Configurar los pines como entradas
for pin in pins:
    GPIO.setup(pin, GPIO.IN)

try:
    while True:
        # Leer y mostrar el estado de cada pin
        for pin in pins:
            estado = GPIO.input(pin)
            print(f"Pin {pin}: {'Alto' if estado else 'Bajo'}")
        
        time.sleep(1)  # Esperar 1 segundo entre lecturas

except KeyboardInterrupt:
    print("Programa terminado por el usuario.")

finally:
    GPIO.cleanup()  # Limpiar la configuración de GPIO al finalizar
