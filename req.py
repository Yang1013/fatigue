import requests
import time

while True:
   time.sleep(60.0)
   load = {'Authorization': 'SharedAccessSignature sr=no-66-2-project.azure-devices.net%2Fdevices%2FRpi1&sig=mKSEHvMn2zP3O4WPh2RxD07kV9%2FLVwx1Wr%2BxbJITF5o%3D&se=1522906577' , 'Content-Type':'application/json'}
   with open("detect.txt", 'r') as f:
      payload = f.read()
   r = requests.post('https://no-66-2-project.azure-devices.net/devices/Rpi1/messages/events?api-version=2016-02-03', headers=load, json=payload)