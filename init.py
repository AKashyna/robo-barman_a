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
        
    '''   
    1. Sex on the Beach
60 ml wódki
70 ml soku pomarańczowego
70 ml soku żurawinowego
50 ml soku ananasowego

    2. Mai Tai
90 ml jasnego rumu
40 ml soku z limonki
80 ml sok pomarańczowy
40 ml sok ananasowy

    3. Mojito
70 ml jasnego rumu
30 ml soku z limonki
150 ml sprite

    4. Cosmopolitan
70 ml wódki
70 ml soku pomarańczowego
70 ml soku żurawinowego
40 ml soku z limonki

    5. Blue Lagoon
65 ml rum
35 ml curacao
150 ml sprite

    6. kamikadze
70 ml wodka
90 ml curacao
90 ml sok limonkowy

    7. Tropical Fire
100 ml rum
75 ml sok żurawinowy
75 ml sok ananasowy
    
    8. THE END
50 ml wódka
50 ml rum

Składniki:
    1 wódka
    2 rum
    3 sok pomarańczowy
    4 sok żurawinowy
    5 sok limonkowy
    6 sok ananasowy
    7 sprite
    8 curacao
    '''
    # Dodawanie drinków
    dodaj_drink("Sex on the Beach")
    dodaj_drink("Mai Tai")
    dodaj_drink("Mojito")
    dodaj_drink("Gin z Tonikiem")
    dodaj_drink("Cosmopolitan")
    dodaj_drink("Blue Lagoon")
    dodaj_drink("kamikadze")
    dodaj_drink("Tropical Fire")
    dodaj_drink("THE END")

    # Dodawanie składników
    dodaj_skladnik("wódka", 1000)
    dodaj_skladnik("rum", 1000)
    dodaj_skladnik("sok pomarańczowy", 1000)
    dodaj_skladnik("sok żurawinowy", 1000)
    dodaj_skladnik("sok limonkowy", 1000)
    dodaj_skladnik("sok ananasowy", 1000)
    dodaj_skladnik("sprite", 2000)
    dodaj_skladnik("curacao", 490)

    # Przypisywanie składników do drinków
        #1. Sex on the Beach
    dodaj_drink_skladnik(1, 1, 60)
    dodaj_drink_skladnik(1, 3, 70)
    dodaj_drink_skladnik(1, 4, 70)
    dodaj_drink_skladnik(1, 6, 50)
        #2. Mai Tai
    dodaj_drink_skladnik(2, 2, 90)
    dodaj_drink_skladnik(2, 5, 40)
    dodaj_drink_skladnik(2, 3, 80)
    dodaj_drink_skladnik(2, 6, 40)
        #3. Mojito
    dodaj_drink_skladnik(3, 2, 70)
    dodaj_drink_skladnik(3, 5, 30)
    dodaj_drink_skladnik(3, 7, 150)
        #4. Cosmopolitan
    dodaj_drink_skladnik(4, 1, 70)
    dodaj_drink_skladnik(4, 3, 70)
    dodaj_drink_skladnik(4, 4, 70)
    dodaj_drink_skladnik(4, 5, 40)
        #5. Blue Lagoon
    dodaj_drink_skladnik(5, 2, 65)
    dodaj_drink_skladnik(5, 8, 35)
    dodaj_drink_skladnik(5, 7, 150)
        #6. Kamikadze
    dodaj_drink_skladnik(6, 1, 70)
    dodaj_drink_skladnik(6, 8, 90)
    dodaj_drink_skladnik(6, 5, 90)
        #7. Tropical Fire
    dodaj_drink_skladnik(7, 2, 100)
    dodaj_drink_skladnik(7, 4, 75)
    dodaj_drink_skladnik(7, 6, 75)
        #8. THE END
    dodaj_drink_skladnik(8, 1, 50)
    dodaj_drink_skladnik(8, 2, 50)


    # Zatwierdzenie zmian i zamknięcie połączenia
    conn.commit()
    conn.close()
    print("Baza danych została zainicjalizowana.")

if __name__ == "__main__": 
    initialize_database()
