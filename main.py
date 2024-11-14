import RPi.GPIO as GPIO
import time

# Definiowanie pinów
pins = [10, 11, 2, 3, 4, 5, 6, 7]

# Ustawienie numeracji pinów GPIO
GPIO.setmode(GPIO.BCM)

# Ustawienie pinów jako wyjścia i włączenie stanu HIGH
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

try:
    # Główna pętla
    while True:
        # Przełączenie wszystkich pinów na stan LOW
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(1)  # Możesz dodać opóźnienie, jeśli jest potrzebne

except KeyboardInterrupt:
    # Czyszczenie ustawień GPIO w przypadku przerwania działania skryptu
    GPIO.cleanup()
