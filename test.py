import smbus2
import time

# Adres wyświetlacza I2C
I2C_ADDR = 0x27  # Sprawdź poprawny adres poleceniem i2cdetect -y 1
bus = smbus2.SMBus(1)

# Definicje LCD
LCD_CMD = 0  # Tryb polecenia
LCD_CHR = 1  # Tryb znaków
ENABLE = 0b00000100  # Bit włączający
BACKLIGHT = 0b00001000  # Podświetlenie włączone

# Adresy linii LCD
LCD_LINE_1 = 0x80  # Adres pierwszej linii
LCD_LINE_2 = 0xC0  # Adres drugiej linii


def lcd_toggle_enable(data):
    """Przełączanie bitu ENABLE."""
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (data | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (data & ~ENABLE))
    time.sleep(0.0005)


def lcd_byte(data, mode):
    """Wysyłanie danych do wyświetlacza."""
    high = mode | (data & 0xF0) | BACKLIGHT
    low = mode | ((data << 4) & 0xF0) | BACKLIGHT
    bus.write_byte(I2C_ADDR, high)
    lcd_toggle_enable(high)
    bus.write_byte(I2C_ADDR, low)
    lcd_toggle_enable(low)


def lcd_init():
    """Inicjalizacja wyświetlacza."""
    lcd_byte(0x33, LCD_CMD)  # Inicjalizacja w trybie 4-bitowym
    lcd_byte(0x32, LCD_CMD)  # Tryb 4-bitowy
    lcd_byte(0x06, LCD_CMD)  # Przesunięcie kursora w prawo
    lcd_byte(0x0C, LCD_CMD)  # Włącz wyświetlacz, wyłącz kursor
    lcd_byte(0x28, LCD_CMD)  # 2 linie, tryb 5x8 znaków
    lcd_byte(0x01, LCD_CMD)  # Wyczyść ekran
    time.sleep(0.005)


def lcd_string(message, line):
    """Wyświetlanie tekstu na LCD."""
    message = message.ljust(16, " ")  # Wyrównanie do 16 znaków
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)


def main():
    """Główna funkcja."""
    lcd_init()  # Inicjalizacja wyświetlacza

    # Wyświetlanie tekstu
    lcd_string("Hello, World!", LCD_LINE_1)
    lcd_string("LCD Test OK!", LCD_LINE_2)

    time.sleep(5)  # Zatrzymanie na 5 sekund

    # Wyświetlenie nowego tekstu
    lcd_byte(0x01, LCD_CMD)  # Wyczyść ekran
    lcd_string("Raspberry Pi", LCD_LINE_1)
    lcd_string("I2C działa!", LCD_LINE_2)


if __name__ == "__main__":
    main()
