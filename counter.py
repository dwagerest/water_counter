
import OPi.GPIO as GPIO
import threading
import paho.mqtt.client as mqtt



def summ():
    global run_now
 

def file_edit(file_name):
        print(f"run file_edit for {file_name}")
        with open(file_name, 'r+') as f:
          current_count = int(f.readlines()[-1])           
          current_count += 1
          print(current_count)
          f.write(f"\n {current_count}")

def my_callback(channel):  
    global is_run_now
    print("run my_callback")
    
    if(is_run_now==0):
        file_edit("cold_clicks.txt")

          
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")


def on_disconnect(client, userdata, rc):
        print("Unexpected MQTT disconnection. Will auto-reconnect")


channel = 3 #номер пина в orange
is_run_now = 0 #запущен ли процесс увеличения счетчика
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel, GPIO.BOTH, callback = my_callback)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
with open(".secret", 'r+') as f:
    #
    data = f.readlines()
    username = data[1].strip()
    adress = data[0].strip()
    password = data[2].strip()
    print(f"{adress}{username}{password}")
client.username_pw_set(username, password)
client.connect(adress, 1883, 60)
f.close()
client.loop_forever()



