import sqlite3

#Funkcja inicjalizująca bazę danych 'drinks.db'
def initialize_database(): 
    # Tworzenie połączenia z bazą danych
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    
    # Usuwanie istniejących tabel
    cursor.execute("DROP TABLE IF EXISTS drink")
    cursor.execute("DROP TABLE IF EXISTS ingredient")
    cursor.execute("DROP TABLE IF EXISTS drink_ingredient")
    cursor.execute("DROP TABLE IF EXISTS order_history")

    # Tworzenie tabel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drink (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drink_ingredient (
        drink_id INTEGER,
        ingredient_id INTEGER,
        amount INTEGER,
        PRIMARY KEY (drink_id, ingredient_id),
        FOREIGN KEY(drink_id) REFERENCES drink(id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredient(id)
    )
    """)  
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drink_id INTEGER,
        FOREIGN KEY(drink_id) REFERENCES drink(id)
    )
    """)
    
    # Dodawanie danych
    def dodaj_drink(name):
        cursor.execute("INSERT INTO drink (name) VALUES (?)", (name,))
    def dodaj_skladnik(name, quantity):
        cursor.execute("INSERT INTO ingredient (name, quantity) VALUES (?, ?)", (name, quantity))
    def dodaj_drink_skladnik(drink_id, ingredient_id, amount):
        cursor.execute("INSERT INTO drink_ingredient (drink_id, ingredient_id, amount) VALUES (?, ?, ?)", (drink_id, ingredient_id, amount))
        
    # Dodawanie drinków
    dodaj_drink("Mojito")
    dodaj_drink("Whisky z Colą")
    dodaj_drink("Wódka z Colą")
    dodaj_drink("Gin z Tonikiem")
    dodaj_drink("Sex on the Beach")

    1. Sex on the Beach
40 ml wódki
50 ml soku pomarańczowego
50 ml soku żurawinowego

    2. Mai Tai
60 ml jasnego rumu
20 ml soku z limonki
50 ml sok pomarańczowy
sok ananasowy?  

    3. Mojito
40 ml jasnego rumu
20 ml soku z limonki
100 ml sprite

    4. Cosmopolitan
40 ml wódki
15 ml soku pomarańczowego
15 ml soku żurawinowego
10 ml soku z limonki

    5. Tom Collins/Gin Fizz
50 ml gin
20 ml sok z limonki
30 ml sprite

    wódka
    rum
    gin
    sok pomarańczowy
    sok żurawinowy
    sok limonkowy
    sprite

    # Dodawanie składników
    dodaj_skladnik("Rum", 1500)
    dodaj_skladnik("Whisky", 1500)
    dodaj_skladnik("Cola", 1500)
    dodaj_skladnik("Wódka", 1500)
    dodaj_skladnik("Gin", 1500)
    dodaj_skladnik("Tonik", 1500)
    dodaj_skladnik("Sok pomarańczowy", 2000)
    dodaj_skladnik("Grenadyna", 1500)

    # Przypisywanie składników do drinków
    dodaj_drink_skladnik(2, 1, 100)  
    dodaj_drink_skladnik(2, 2, 200)  
    dodaj_drink_skladnik(3, 3, 100)  
    dodaj_drink_skladnik(3, 2, 200)  
    dodaj_drink_skladnik(4, 4, 100)  
    dodaj_drink_skladnik(4, 5, 200)  
    dodaj_drink_skladnik(5, 3, 100)  
    dodaj_drink_skladnik(5, 6, 150) 
    dodaj_drink_skladnik(5, 7, 50)   
    dodaj_drink_skladnik(1, 1, 50)   

    # Zatwierdzenie zmian i zamknięcie połączenia
    conn.commit()
    conn.close()
    print("Baza danych została zainicjalizowana.")

if __name__ == "__main__": 
    initialize_database()

