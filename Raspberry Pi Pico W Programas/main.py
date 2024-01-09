import time
import ubinascii
from umqtt.simple import MQTTClient
from easy_comms import Easy_comms
from time import sleep
import machine
import ujson

# Default MQTT_BROKER para conectarse a
MQTT_BROKER = "11.1.15.43"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SUBSCRIBE_TOPIC = b"temperature"
PUBLISH_TOPIC = b"temperature"

# Publicar mensajes MQTT despues de cada tiempo de espera
last_publish = time.time()
publish_interval = 5

#parametros uart
com1 = Easy_comms(uart_id=0, baud_rate=115200, tx=16, rx=17)
com1.start()

#Resetea el dispositivo en caso de error
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def get_sensor_reading():
    message = com1.read()
    if message is None:
        return None
    temperatures = message.split('\n')  # Dividir la cadena en una lista
    #convertir cada item de la lista en un valor flotante
    temperatures = [float(temp) for temp in temperatures if temp and temp.replace('.', '', 1).isdigit()]  
    return temperatures

# Programa principal
def main():
    print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(SUBSCRIBE_TOPIC)
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")
    while True:
        # espera del mensaje sin bloqueo
        mqttClient.check_msg()
        global last_publish
        current_time = time.time()
        if (current_time - last_publish) >= publish_interval:
            temperatures = get_sensor_reading()
            if temperatures is not None:
                for temp in temperatures:
                    readings = {"temperature": round(temp,2)}
                    print(f"mensaje recibido: {ujson.dumps(readings)}")
                    mqttClient.publish(PUBLISH_TOPIC, ujson.dumps(readings).encode())
            last_publish = current_time
        time.sleep(1)

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()