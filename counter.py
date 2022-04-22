import OPi.GPIO as GPIO
import threading
import paho.mqtt.client as mqtt
import enum

@enum.unique
class WaterChannel(enum.Enum):
    cold = 3
    hot = 5


def summ(channel):
    print(f"run summ for {WaterChannel._value2member_map_[channel].name}")
    global is_run_now
    value = file_edit_up(channel, "value")
    water_topic = "orange/bathroom/" + WaterChannel._value2member_map_[channel].name + "water"
    print (water_topic)
    client.publish(topic = water_topic, payload = value, qos=0, retain=False)
    is_run_now = 0
    
 

def file_edit_up(channel, type):
        file_name = WaterChannel._value2member_map_[channel].name + "_" + type + ".txt"
        print(f"run file_edit for {file_name}")
        with open(file_name, 'r+') as f:
          current_count = int(f.readlines()[-1])           
          current_count += 1
          print(current_count)
          f.write(f"\n {current_count}")
          print("\n")
          return current_count


def my_callback(channel):  
    print(f"сработал канал {WaterChannel._value2member_map_[channel].name}")
    global is_run_now    
    file_edit_up(channel, "clicks")
    buzzing_timer = threading.Timer(1, summ, [channel])
    if(is_run_now == 0):
        is_run_now = 1
        buzzing_timer.start()
        

          
        

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("orange/bathroom/calibrate")
    


def on_message(client, userdata, msg):
    if(msg.topic == 'orange/bathroom/calibrate'):
        msg.payload = msg.payload.decode("utf-8")
        body = msg.payload.split()
        file_name = body[0] + "_" + body[1] + ".txt"
        with open(file_name, 'w') as f:
            print(f"калибровка {file_name}, значение {body[2]}")
            f.write(f"\n {body[2]}")
            print("\n")   

        



def on_disconnect(client, userdata, rc):
        print("Unexpected MQTT disconnection. Will auto-reconnect")


# cold_water_channel = 3 #номер пина в orange
# hot_water_channel = 5 #номер пина в orange

is_run_now = 0 #запущен ли процесс увеличения счетчика

GPIO.setmode(GPIO.BOARD)
GPIO.setup([WaterChannel.cold.value, WaterChannel.hot.value], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(WaterChannel.cold.value, GPIO.BOTH, callback = my_callback)
GPIO.add_event_detect(WaterChannel.hot.value, GPIO.BOTH, callback = my_callback)

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



