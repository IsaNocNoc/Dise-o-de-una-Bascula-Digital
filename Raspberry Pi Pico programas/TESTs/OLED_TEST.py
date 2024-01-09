from machine import Pin, I2C,Timer
from utime import sleep_ms
import utime
from ssd1306 import SSD1306_I2C
from hx711_2 import HX711_2
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

def plot_time(yp, t, x, y, var=[0.0,22.0], vpts=[25,16,40], hpts=[25,55,112]):
    """
    la grafica de la funcion trabaja de la siguiente forma:
    yp: nustra dependiente varaible
    t: tiempo
    x: lista de las dos posiciones de nuestra variable x, siendo x[0] la posicion pasada y x[1] la posicion futura
    y: lista de las dos posiciones de nuestra variable y, siendo y[0] la posicion pasada e y[1] la posicion futura
    var =[a,b]: contendra la magnitud de nuestra varaible (se ajusta la peso maximo de nuestro sensor)
    vpts =[a,b,c]: pixeles/puntos de nuestra arista vertical
    hpts =[a,b,c]: pixeles/ puntos de nuestra arista horizontal
    
    nuestras varaibles t,x,y son declaradas en nuestra parte principal del programa
    
    yp sera el valor del peso leido
    """
    #declaracion de aristas
    oled.vline(vpts[0],vpts[1],vpts[2],1)
    oled.hline(hpts[0],hpts[1],hpts[2],1)
    #declaracion de nuestros limites de la varaible var
    oled.text(str(round(var[0],1)),vpts[0]-25,hpts[1]-5)
    oled.text(str(round(var[1],1)),vpts[0]-25,vpts[1])
    
    #interpolazion
    y[1]=int((yp-var[0])/(var[1]-var[0])*(vpts[1]-hpts[1])+hpts[1])
    if t < hpts[2]-hpts[0]:
        x[1]=x[0]+1
    else:
        x[1]=hpts[2]
    
    #grafico de nuestra linea
    oled.line(x[0],y[0],x[1],y[1],1)
    oled.show()
    
    #actualiza los valores pasados
    y[0]=y[1]
    x[0]=x[1]
    
    #si la grafica ya alcanzo el final: 
    if t > hpts[2] -hpts[0]:
        #borra los primeros pixeles de la grafica
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0)
        #borra toda el eje y sus leyendas
        oled.fill_rect(vpts[0]-25,vpts[1], vpts[0], vpts[2]+5,0)
        #Desplaya los elementos en x a la izquierda
        oled.scroll(-1,0)
        #Se vuelve a incluir los elementos borrados
        oled.vline(vpts[0],vpts[1],vpts[2],1)
        oled.hline(hpts[0],hpts[1],hpts[2],1)
        oled.text(str(round(var[0],1)),vpts[0]-25,hpts[1]-5)
        oled.text(str(round(var[1],1)),vpts[0]-25,vpts[1])
    #si la grafica aun no llega a su final
    else:
        t+=1
        
    return t,x,y

#programa principal
if __name__=='__main__':
    
     i2c = I2C(1, scl=Pin(15), sda=Pin(14))
     oled = SSD1306_I2C(128,64,i2c)
    
     t=0
     y=[55,55]
     x=[25,25]
     
     pd_sck = Pin(16, Pin.OUT)
     dout = Pin(17, Pin.IN)

     hx = HX711_2(pd_sck, dout)
     hx.tare()
     hx.set_scale(10800)
     
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
#declaracion de las funciones del Led y el buzzer         
     def blink(timer):
         led.toggle()
         
     def buzzer_and_led():
         buzzer.value(1)
         led.value(1)
         utime.sleep(0.28)
         buzzer.value(0)
         timer.deinit()
         led.value(0)
         
     timer=Timer()
         
     led=Pin(12,Pin.OUT)
     buzzer= Pin(13,Pin.OUT)
     buzzer.value(0)
     led.value(0)

#ciclo principal     
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
        t,x,y=plot_time(weight,t,x,y)
        oled.fill_rect(0,0,120,15,0)
        oled.text("Weight: ", 0,0)
        oled.text(str(round(weight,1)),58,0)
        oled.show()
        sleep_ms(100)