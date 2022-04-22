import OPi.GPIO as GPIO
import threading
import paho.mqtt.client as mqtt
import enum

@enum.unique
class WaterChannel(enum.Enum):
    cold_water_channel = 3
    hot_water_channel = 5


def summ():
    print("run summ")
    global is_run_now
    value = file_edit_up("cold_value.txt")
    client.publish(topic = 'orange/bathroom/coldwater', payload = value, qos=0, retain=False)
    is_run_now = 0
    
 

def file_edit_up(file_name):
        print(f"run file_edit for {file_name}")
        with open(file_name, 'r+') as f:
          current_count = int(f.readlines()[-1])           
          current_count += 1
          print(current_count)
          f.write(f"\n {current_count}")
          print("\n")
          return current_count


def my_callback(channel):  
    print(f"канал: {WaterChannel._value2member_map_[channel].name}")
    global is_run_now    
    print("run my_callback\n")    
    file_edit_up("cold_clicks.txt")
    buzzing_timer = threading.Timer(1, summ)
    if(is_run_now == 0):
        is_run_now = 1
        buzzing_timer.start()
        

          
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic == 'orange/bathroom/coldwater':
        print("catch")



def on_disconnect(client, userdata, rc):
        print("Unexpected MQTT disconnection. Will auto-reconnect")


# cold_water_channel = 3 #номер пина в orange
# hot_water_channel = 5 #номер пина в orange

is_run_now = 0 #запущен ли процесс увеличения счетчика

GPIO.setmode(GPIO.BOARD)
GPIO.setup([WaterChannel.cold_water_channel.value, WaterChannel.hot_water_channel.value], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(WaterChannel.cold_water_channel.value, GPIO.BOTH, callback = my_callback)
GPIO.add_event_detect(WaterChannel.hot_water_channel.value, GPIO.BOTH, callback = my_callback)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
with open(".secret", 'r') as f:
    data = f.readlines()
    username = data[1].strip()
    adress = data[0].strip()
    password = data[2].strip()
    client.username_pw_set(username, password)
client.connect(adress, 1883, 60)
f.close()
client.loop_forever()



