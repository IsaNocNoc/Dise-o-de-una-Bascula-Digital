from machine import Pin
from hx711_2 import HX711_2

# Configuracion de los pines de datos y reloj
pd_sck = Pin(16, Pin.OUT)
dout = Pin(17, Pin.IN)

# Instancia de la clase HX711_2
hx = HX711_2(pd_sck, dout)

# Calibracion la celda de carga
hx.tare()

# Escala para una galga extensiométrica de 20 kg
hx.set_scale(10800)

# Inicialización del valor suavizado
smoothed_weight = 0.0
alpha = 0.2  # Factor de suavizado, ajusta según sea necesario

while True:
    # Lee el peso en unidades (kg)
    raw_weight = hx.get_units()
    if raw_weight < 0:
        raw_weight = 0.0
    
    # Aplica suavizado exponencial
    smoothed_weight = alpha * raw_weight + (1 - alpha) * smoothed_weight
    
    # Muestra el peso suavizado en la consola
    print("Peso Suavizado: {:.2f} kg".format(smoothed_weight))