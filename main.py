import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
import threading

# Konfiguracja GPIO
pins = [10, 11, 2, 3, 4, 5, 6, 7]  # GPIO piny dla pomp
flow_rates = [10] * len(pins)  # Przepływ (ml/s) dla każdej pompy
fluid_data = [0] * len(pins)  # Przelana ilość płynu (ml) dla każdej pompy

GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def run_pump(pin_index, duration):
    """
    Funkcja włącza pompę na określony czas i aktualizuje ilość przepompowanego płynu.
    :param pin_index: Indeks pinu (od 0 do len(pins)-1).
    :param duration: Czas pracy pompy w sekundach.
    """
    pin = pins[pin_index]
    flow_rate = flow_rates[pin_index]
    
    GPIO.output(pin, GPIO.LOW)  # Włączenie pompy
    time.sleep(duration)  # Praca przez określony czas
    GPIO.output(pin, GPIO.HIGH)  # Wyłączenie pompy
    
    # Aktualizacja ilości przepompowanego płynu
    fluid_data[pin_index] += flow_rate * duration

def pump_sequence():
    """
    Funkcja uruchamiająca pompy w sekwencji.
    """
    while True:
        for i in range(len(pins)):
            run_pump(i, 5)  # Włączenie każdej pompy na 5 sekund
            time.sleep(1)  # Krótkie opóźnienie przed następną pompą

# Uruchomienie sekwencji pomp w osobnym wątku
pump_thread = threading.Thread(target=pump_sequence, daemon=True)
pump_thread.start()

# Konfiguracja Flask
app = Flask(__name__)

@app.route("/")
def index():
    # Tworzenie wykresu z użyciem danych z pomp
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"Pompa {i+1}" for i in range(len(pins))],
                         y=fluid_data,
                         name="Przepompowany płyn (ml)"))
    fig.update_layout(title="Ilość przelanego płynu przez pompy",
                      xaxis_title="Pompa",
                      yaxis_title="Przepompowana ilość płynu (ml)")
    graph_html = pio.to_html(fig, full_html=False)
    
    return f"""
    <html>
        <head>
            <title>Monitorowanie pomp</title>
        </head>
        <body>
            <h1>Monitorowanie przepompowanego płynu</h1>
            {graph_html}
        </body>
    </html>
    """

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program zakończony. GPIO wyczyszczone.")
