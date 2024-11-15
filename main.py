import RPi.GPIO as GPIO
import time
import sqlite3
from flask import Flask, request, redirect, url_for
import plotly.graph_objects as go
import plotly.io as pio

# Konfiguracja GPIO
pins = [10, 11, 2, 3, 4, 5, 6, 7]  # GPIO piny dla pomp
flow_rate = 100  # 4.17  # Przepływ (ml/s)
fluid_data = [0] * len(pins)  # Przelana ilość płynu dla każdej pompy

GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Mapowanie składników na piny pomp
ingredient_to_motor_map = {
    "Whisky": 0, #10
    "Cola": 1, #11
    "Wódka": 2, #2
    "Gin": 3, #3
    "Tonik": 4, #4
    "Sok pomarańczowy": 5, #5
    "Grenadyna": 6, #6
    "Rum": 7 #7
}

# Funkcje do obsługi pomp
def run_pump(pin, work_time):
    GPIO.output(pins[pin], GPIO.LOW)
    time.sleep(work_time)
    GPIO.output(pins[pin], GPIO.HIGH)
    fluid_data[pin] += flow_rate * work_time

def make_drink(drink):
    with sqlite3.connect('drinks.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ingredient.name, drink_ingredient.amount, ingredient.quantity  
            FROM drink_ingredient
            JOIN ingredient ON drink_ingredient.ingredient_id = ingredient.id
            WHERE drink_ingredient.drink_id = ?
        """, (drink,))
        ingredients = cursor.fetchall()

        for ingredient, amount, quantity in ingredients:
            if quantity < amount:
                raise ValueError(f"Brak wystarczającej ilości składnika: {ingredient}")

        for ingredient, amount, quantity in ingredients:
            motor_index = ingredient_to_motor_map.get(ingredient)
            if motor_index is not None:
                run_pump(motor_index, amount / flow_rate)
            cursor.execute("UPDATE ingredient SET quantity = quantity - ? WHERE name = ?", (amount, ingredient))

        cursor.execute("INSERT INTO order_history (drink_id) VALUES (?)", (drink,))
        conn.commit()


# Flask aplikacja
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        drink = int(request.form.get("drink_id"))
        try:
            make_drink(drink)
        except ValueError as e:
            return str(e)
        return redirect(url_for("index"))

    # Pobieranie listy drinków
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM drink")
    drinks = cursor.fetchall()
    cursor.execute("""
        SELECT drink.name, COUNT(order_history.drink_id) as count
        FROM order_history
        JOIN drink ON order_history.drink_id = drink.id
        GROUP BY drink.id
        ORDER BY count DESC
    """)
    drink_stats = cursor.fetchall()
    drink_names = [row[0] for row in drink_stats]
    drink_counts = [row[1] for row in drink_stats]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=drink_names, y=drink_counts, name="Najczęściej robione drinki"))
    fig1.update_layout(title="Statystyka najczęściej robionych drinków", xaxis_title="Drink", yaxis_title="Ilość")

    # Wykres 2: Ilości składników w magazynie
    cursor.execute("SELECT name, quantity FROM ingredient")
    ingredients = cursor.fetchall()
    ingredient_names = [row[0] for row in ingredients]
    ingredient_quantities = [row[1] for row in ingredients]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=ingredient_names, y=ingredient_quantities, name="Pozostałe składniki"))
    fig2.update_layout(title="Pozostała ilość składników w magazynie", xaxis_title="Składnik", yaxis_title="Ilość (ml)")

    conn.close()

    # wykres 3
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"{i}" for i, j in ingredient_to_motor_map.items()],
                         y=fluid_data,
                         name="Przepompowany płyn (ml)"))
    fig.update_layout(title="Ilość przelanego płynu przez pompy",
                      xaxis_title="Składnik",
                      yaxis_title="Przepompowana ilość płynu (ml)")

    graph_html = pio.to_html(fig, full_html=False)
    graph_html1 = pio.to_html(fig1, full_html=False)
    graph_html2 = pio.to_html(fig2, full_html=False)
    # Generowanie strony
    return f"""
    <html>
        <head>
            <title>Robo-Barman</title>
            <style>
                .container {{
                    display: flex;
                    flex-direction: row;
                    align-items: flex-start;
                }}
                .buttons {{
                    margin-right: 20px;
                }}
                .chart {{
                    flex-grow: 1;
                }}
            </style>
        </head>
        <body>
            <h1>Robo-Barman: Wybierz Drink</h1>
            <div class="container">
                <div class="buttons">
                    <h2>Dostępne Drinki</h2>
                    {''.join([f'''
                    <form method="POST">
                        <input type="hidden" name="drink_id" value="{drink[0]}">
                        <button type="submit">{drink[1]}</button>
                    </form>
                    ''' for drink in drinks])}
                </div>
                <div class="chart">
                    {graph_html}
                    {graph_html1}
                    {graph_html2}
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program zakończony.")