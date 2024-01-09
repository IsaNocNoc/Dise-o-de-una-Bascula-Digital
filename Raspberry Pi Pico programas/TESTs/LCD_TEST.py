from machine import Pin, I2C
from hx711_2 import HX711_2
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Dirección del I2C y tamaño del LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Raspberry Pi Pico
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=600000)

# Configuración LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)

# Configuracion de los pines de datos y reloj
pd_sck = Pin(16, Pin.OUT)
dout = Pin(17, Pin.IN)

# Instancia de la clase HX711_2
hx = HX711_2(pd_sck, dout)

# Calibracion la celda de carga
hx.tare()

# Escala para una galga extensiométrica de 20 kg
hx.set_scale(10800)

while True:
    # Lee el peso en unidades (kg)
    weight = hx.get_units()

    # Mostrar el peso como cero si es negativo
    if weight < 0:
        weight = 0.0
    
    # Muestra el peso en la consola
    print("Peso: {:.2f} kg".format(weight))
    lcd.clear()
    lcd_str("Conteo: {:.2f} kg".format(weight), 0, 0)