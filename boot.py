import machine
from machine import Pin, I2C

import dht
import network
import urequests
from time import sleep

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'YOUR_SSID'
password = 'YOUR_PASSWORD'


ms_sleep_time = 3600000

sensor = dht.DHT11(Pin(14))

rain = Pin(12, Pin.IN)

led = Pin(2, Pin.OUT)
led.on()

api_key = 'YOUR_IFTTT_API_KEY'


station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())




def deep_sleep(msecs) :
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  rtc.alarm(rtc.ALARM0, msecs)

  machine.deepsleep()


try:

    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()

    sensor_readings = {'value1':temp, 'value2':hum, 'value3':rain.value()}
    print(sensor_readings)

    request_headers = {'Content-Type': 'application/json'}

    request = urequests.post(
        'http://maker.ifttt.com/trigger/tempandhumlogger/with/key/' + api_key,
        json=sensor_readings,
        headers=request_headers)
    print(request.text)
    request.close()
except OSError as e:
    print('Failed to read/publish sensor readings.')

sleep(10)

led.off()

deep_sleep(ms_sleep_time)
