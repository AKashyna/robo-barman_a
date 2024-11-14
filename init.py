import sqlite3

def initialize_database():
    """
    Funkcja inicjalizująca bazę danych 'drinks.db' i dodająca przykładowe dane.
    """
    # Tworzenie połączenia z bazą danych
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    
    
    # Usuwanie istniejących tabel (jeśli istnieją)
    cursor.execute("DROP TABLE IF EXISTS drink")
    cursor.execute("DROP TABLE IF EXISTS ingredient")
    cursor.execute("DROP TABLE IF EXISTS drink_ingredient")
    cursor.execute("DROP TABLE IF EXISTS drink_statistics")

    # Tworzenie tabel, jeśli nie istnieją
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drink_id INTEGER,
        ingredient_id INTEGER,
        amount INTEGER,
        FOREIGN KEY(drink_id) REFERENCES drink(id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredient(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drink_statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drink_id INTEGER,
        FOREIGN KEY(drink_id) REFERENCES drink(id)
    )
    """)
    

    # Dodawanie przykładowych danych
    def dodaj_drink(name):
        cursor.execute("INSERT INTO drink (name) VALUES (?)", (name,))

    def dodaj_skladnik(name, quantity):
        cursor.execute("INSERT INTO ingredient (name, quantity) VALUES (?, ?)", (name, quantity))

    def dodaj_drink_skladnik(drink_id, ingredient_id, amount):
        cursor.execute("INSERT INTO drink_ingredient (drink_id, ingredient_id, amount) VALUES (?, ?, ?)", 
                       (drink_id, ingredient_id, amount))
        

    # Dodawanie drinków
    dodaj_drink("Mojito")
    dodaj_drink("Whisky z Colą")
    dodaj_drink("Wódka z Colą")
    dodaj_drink("Gin z Tonikiem")
    dodaj_drink("Sex on the Beach")

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
    dodaj_drink_skladnik(2, 1, 100)  # Mojito: Whisky
    dodaj_drink_skladnik(2, 2, 200)  # Mojito: Cola
    dodaj_drink_skladnik(3, 3, 100)  # Wódka z Colą: Wódka
    dodaj_drink_skladnik(3, 2, 200)  # Wódka z Colą: Cola
    dodaj_drink_skladnik(4, 4, 100)  # Gin z Tonikiem: Gin
    dodaj_drink_skladnik(4, 5, 200)  # Gin z Tonikiem: Tonik
    dodaj_drink_skladnik(5, 3, 100)  # Sex on the Beach: Wódka
    dodaj_drink_skladnik(5, 6, 150)  # Sex on the Beach: Sok pomarańczowy
    dodaj_drink_skladnik(5, 7, 50)   # Sex on the Beach: Grenadyna
    dodaj_drink_skladnik(1, 1, 50)   # Mojito: Rum


    # Zatwierdzenie zmian i zamknięcie połączenia
    conn.commit()
    conn.close()
    print("Baza danych została zainicjalizowana.")
    
initialize_database()

