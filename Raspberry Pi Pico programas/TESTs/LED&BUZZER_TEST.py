1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
import _thread
import machine
import utime

# Configura el pin GPIO para el LED
led_pin = machine.Pin(12, machine.Pin.OUT)

# Configura el pin GPIO para el buzzer
buzzer_pin = machine.Pin(13, machine.Pin.OUT)

# Variable global para controlar el estado del LED y el buzzer
estado = 0

# Función para el parpadeo del LED a 20Hz
def parpadear_led():
    global estado
    while True:
        if estado == 1:
            led_pin.value(1)  # Enciende el LED
            utime.sleep(0.025)  # Espera 25ms (1/40 de segundo)
            led_pin.value(0)  # Apaga el LED
            utime.sleep(0.025)  # Espera 25ms (1/40 de segundo)
        else:
            led_pin.value(0)  # Apaga el LED

# Función para activar el buzzer durante 2 segundos
def activar_buzzer():
    global estado
    estado = 1
    buzzer_pin.value(1)  # Enciende el buzzer
    utime.sleep(2)  # Mantén el buzzer activado durante 2 segundos
    buzzer_pin.value(0)  # Apaga el buzzer
    estado = 0

# Iniciar el hilo para el parpadeo del LED
_thread.start_new_thread(parpadear_led, ())

# Ejecutar la función para activar el buzzer
activar_buzzer()