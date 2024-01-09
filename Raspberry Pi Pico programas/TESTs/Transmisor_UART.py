from easy_comms import Easy_comms
from time import sleep

com1 = Easy_comms(uart_id=1, baud_rate=9600, tx=8, rx=9)
com1.start()

count = 0
while True:
    # enviar mensaje
    com1.send(f'hello, {count}')
    
    
    sleep(1)
    count +=1