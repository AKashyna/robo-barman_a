import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
import threading
import sqlite3
def dodaj_drink(name):
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO drink (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def dodaj_skladnik(name, quantity):
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredient (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()

def dodaj_drink_skladnik(drink_id, ingredient_id, amount):
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO drink_ingredient (drink_id, ingredient_id, amount) VALUES (?, ?, ?)", (drink_id, ingredient_id, amount))
    conn.commit()
    conn.close()
# Przykładowe dodawanie drinka i składników
dodaj_drink("Mojito")
dodaj_drink("Whisky z Colą")
dodaj_drink("Wódka z Colą")
dodaj_drink("Gin z Tonikiem")
dodaj_drink("Sex on the Beach")

dodaj_skladnik("Rum", 50)
dodaj_skladnik("Mięta", 30)
dodaj_skladnik("Whisky", 100)
dodaj_skladnik("Cola", 200)
dodaj_skladnik("Wódka", 100)
dodaj_skladnik("Gin", 100)
dodaj_skladnik("Tonik", 200)
dodaj_skladnik("Sok pomarańczowy", 150)
dodaj_skladnik("Grenadyna", 50)

# Załóżmy, że drink_id = 1, składnik_id = 1 i 2
# Whisky z Colą
dodaj_drink_skladnik(1, 1, 100)  # Whisky
dodaj_drink_skladnik(1, 2, 200)  # Cola

# Wódka z Colą
dodaj_drink_skladnik(2, 3, 100)  # Wódka
dodaj_drink_skladnik(2, 2, 200)  # Cola

# Gin z Tonikiem
dodaj_drink_skladnik(3, 4, 100)  # Gin
dodaj_drink_skladnik(3, 5, 200)  # Tonik

# Sex on the Beach
dodaj_drink_skladnik(4, 3, 100)  # Wódka
dodaj_drink_skladnik(4, 6, 150)  # Sok pomarańczowy
dodaj_drink_skladnik(4, 7, 50)   # Grenadyna

#Mohito
dodaj_drink_skladnik(1, 1, 50)  # Dodanie rumu do mojito
dodaj_drink_skladnik(1, 2, 30)  # Dodanie mięty do mojito
# Konfiguracja GPIO
pins = [10, 11, 2, 3, 4, 5, 6, 7]  # GPIO piny dla pomp
flow_rates = [10] * len(pins)  # Przepływ (ml/s) dla każdej pompy
fluid_data = [0] * len(pins)  # Przelana ilość płynu (ml) dla każdej pompy

GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def get_motor_pin_for_ingredient(ingredient_name):
    ingredient_to_motor_map = {
        "Whisky": 0,  
        "Cola": 1,    
        "Wódka": 2,   
        "Gin": 3,     
        "Tonik": 4,   
        "Sok pomarańczowy": 5, 
        "Grenadyna": 6,  
        "Mięta":7,
        "Rum":8
    }
    return ingredient_to_motor_map.get(ingredient_name, -1) 




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
