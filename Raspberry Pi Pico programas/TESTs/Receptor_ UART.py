from easy_comms import Easy_comms
from time import sleep

com1 = Easy_comms(uart_id=0, baud_rate=9600, tx=16, rx=17)
com1.start()

while True:
    message = ""
    message = com1.read()
    
    if message is not None:
        print(f"message received: {message.strip('\n')}")
    sleep(1)  