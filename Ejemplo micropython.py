import machine
import ssd1306
import time
from machine import Pin

# Configurar el objeto I2C para la comunicación con la pantalla OLED
i2c = machine.I2C(1, scl=machine.Pin(15), sda=machine.Pin(14))  # Cambia los pines según tu conexión

# Crear una instancia del objeto SSD1306 para la pantalla OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configurar el pin 25 como salida para el LED
led = Pin(25, Pin.OUT)

while True:
    # Encender el LED
    led.value(1)
    
    # Esperar 2 segundos
    time.sleep(2)
    
    # Apagar el LED
    led.value(0)
    
    # Borrar la pantalla
    oled.fill(0)
    
    # Mostrar "Hola mundo"
    oled.text("Hola Mundo", 0, 0, 1)
    oled.show()
    
    # Esperar un segundo
    time.sleep(1)
