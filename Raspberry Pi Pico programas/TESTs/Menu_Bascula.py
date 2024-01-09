from machine import Pin, I2C, Timer
from time import sleep_ms, sleep
from ssd1306 import SSD1306_I2C
from hx711_2 import HX711_2
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import framebuf

MODO_MAX = 3
global modo
global contador
global hx
global weight

modo = 0
contador = 0
calibracion=False


I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

botones = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in range(2, 5)]
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=600000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
pd_sck = Pin(16, Pin.OUT)
dout = Pin(17, Pin.IN)


hx = HX711_2(pd_sck, dout)
hx.tare()
hx.set_scale(10800)

def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)
         
def blink(timer):
    led.toggle()
 
def buzzer_and_led():
    buzzer.value(1)
    led.value(1)
    sleep_ms(280)
    buzzer.value(0)
    timer.deinit()
    led.value(0)
 
timer=Timer()
 
led=Pin(12,Pin.OUT)
buzzer= Pin(13,Pin.OUT)
buzzer.value(0)
led.value(0)

lcd.clear()
lcd_str("PESO MAX: 20Kg", 0, 0)
sleep_ms(2000)
lcd.clear()

def plot_time(yp, t, x, y, var=[0.0,5.0], vpts=[25,16,40], hpts=[25,55,112]):
    oled.vline(vpts[0],vpts[1],vpts[2],1)
    oled.hline(hpts[0],hpts[1],hpts[2],1)
    oled.text(str(round(var[0],1)),vpts[0]-25,hpts[1]-5)
    oled.text(str(round(var[1],1)),vpts[0]-25,vpts[1])
    
    y[1]=int((yp-var[0])/(var[1]-var[0])*(vpts[1]-hpts[1])+hpts[1])
    if t < hpts[2]-hpts[0]:
        x[1]=x[0]+1
    else:
        x[1]=hpts[2]
    
    oled.line(x[0],y[0],x[1],y[1],1)
    oled.show()
    
    y[0]=y[1]
    x[0]=x[1]
    
    if t > hpts[2] -hpts[0]:
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0)
        oled.fill_rect(vpts[0]-25,vpts[1], vpts[0], vpts[2]+5,0)
        oled.scroll(-1,0)
        oled.vline(vpts[0],vpts[1],vpts[2],1)
        oled.hline(hpts[0],hpts[1],hpts[2],1)
        oled.text(str(round(var[0],1)),vpts[0]-25,hpts[1]-5)
        oled.text(str(round(var[1],1)),vpts[0]-25,vpts[1])
    else:
        t+=1
        
    return t,x,y

def boton_interrupt(pin):
    global modo
    global contador
    
    boton = botones[botones.index(pin)]
    if boton.value():
        modo = botones.index(pin) + 1
        print(modo)
    if modo > MODO_MAX:
        modo = 0
        contador = 0

for boton in botones:
    boton.irq(trigger=Pin.IRQ_RISING, handler=boton_interrupt)

while True:
    weight = hx.get_units()
    if weight < 0:
        weight = 0.0
    if weight >= 20:
        timer.init(freq=25, mode=Timer.PERIODIC, callback=blink)
        buzzer_and_led()
    if weight > 20:
        buzzer.value(0)
    print("Peso: {:.2f} kg".format(weight))
    lcd.clear()
    lcd_str("PESO: {:.2f} kg".format(weight), 0, 0)
    
    oled.fill(0)
    
    if modo == 0:
        oled.text("MENU", 42, 0)
        oled.text("1.- TARA", 0, 16)
        oled.text("2.- CONVRT", 0, 26)
        oled.text("3.- GRAFICA", 0, 36)
        
    elif modo == 1:
        if not calibracion:
            oled.text("Calibracion", 0, 0)
            oled.text("CALIBRANDO...",15,25)
            oled.show()
            sleep_ms(1500)  # Calibración de 1.5 segundos
            hx.tare()
            calibracion = True
            continue
        else:
            calibracion = False
            modo = 0
            contador = 0
        
    elif modo == 2:
        while modo == 2:
            weight = hx.get_units()
            if weight < 0:
                weight = 0.0
            if weight >= 20:
                timer.init(freq=25, mode=Timer.PERIODIC, callback=blink)
                buzzer_and_led()
            if weight > 20:
                buzzer.value(0)
            print("Peso: {:.2f} kg".format(weight))
            lcd.clear()
            lcd_str("PESO: {:.2f} kg".format(weight), 0, 0)
            oled.fill(0)
            oled.text("Conversiones", 10, 0)
            
            # Realiza las conversiones
            kg = weight
            lb = weight / 0.45359237
            oz = weight / 0.02834952
            g = weight * 1000
            
            # Muestra los resultados en el display
            oled.text("Kg: {:.2f} kg".format(kg), 0, 16)
            oled.text("Lbs: {:.2f} lb".format(lb), 0, 26)
            oled.text("Oz: {:.2f} oz".format(oz), 0, 36)
            oled.text("Gr: {:.2f} g".format(g), 0, 46)
            
            oled.show()

            
    elif modo == 3:
        t = 0
        y = [55, 55]
        x = [25, 25]
        
        while modo == 3:
            weight = hx.get_units()
            if weight < 0:
                weight = 0.0
            if weight >= 20:
                timer.init(freq=25, mode=Timer.PERIODIC, callback=blink)
                buzzer_and_led()
            if weight > 20:
                buzzer.value(0)
            print("Peso: {:.2f} kg".format(weight))
            lcd.clear()
            lcd_str("PESO: {:.2f} kg".format(weight), 0, 0)
            t, x, y = plot_time(weight, t, x, y)
            oled.fill_rect(0, 0, 120, 15, 0)
            oled.text("weight: ", 0, 0)
            oled.text(str(round(weight, 1)), 60, 0)
            oled.show()
            sleep_ms(100)
            
    oled.show()
    sleep_ms(100)