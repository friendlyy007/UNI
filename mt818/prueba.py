from flask import Flask, render_template, Response
import pandas as pd
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico')
def grafico():
    # Cargar el archivo CSV con los datos de vibración
    df = pd.read_csv('frequencyFeatures.csv')

    # Filtrar datos para condiciones de buen estado ('on') y mal estado ('unb')
    motor_bueno = df[df['Label'] == 'on']  # Motor en buen estado
    motor_mal = df[df['Label'] == 'unb']  # Motor en mal estado (con desbalance)

    # Crear el gráfico
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))

    # Graficar las vibraciones para el motor en buen estado (condición 'on')
    ax[0].plot(motor_bueno['xAcc010Hz'], label='Vibración X a 10Hz', color='green')
    ax[0].plot(motor_bueno['xAcc015Hz'], label='Vibración X a 15Hz', color='blue')
    ax[0].plot(motor_bueno['xAcc020Hz'], label='Vibración X a 20Hz', color='red')
    ax[0].plot(motor_bueno['xAcc025Hz'], label='Vibración X a 25Hz', color='orange')
    ax[0].set_title('Vibraciones de Motor en Buen Estado')
    ax[0].set_xlabel('Muestras')
    ax[0].set_ylabel('Amplitud de Vibración (g)')
    ax[0].legend()

    # Graficar las vibraciones para el motor en mal estado (condición 'unb')
    ax[1].plot(motor_mal['xAcc010Hz'], label='Vibración X a 10Hz', color='green', linestyle='--')
    ax[1].plot(motor_mal['xAcc015Hz'], label='Vibración X a 15Hz', color='blue', linestyle='--')
    ax[1].plot(motor_mal['xAcc020Hz'], label='Vibración X a 20Hz', color='red', linestyle='--')
    ax[1].plot(motor_mal['xAcc025Hz'], label='Vibración X a 25Hz', color='orange', linestyle='--')
    ax[1].set_title('Vibraciones de Motor en Mal Estado')
    ax[1].set_xlabel('Muestras')
    ax[1].set_ylabel('Amplitud de Vibración (g)')
    ax[1].legend()

    # Ajustar el layout para evitar solapamientos
    plt.tight_layout()

    # Guardar la figura en un buffer de memoria
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)

    # Devolver la imagen como respuesta
    return Response(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
