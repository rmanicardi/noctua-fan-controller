import pigpio
import time
import signal
import sys
import os

# Configuration
FAN_PIN = 18            # BCM pin used to drive PWM fan
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 25000        # [Hz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 40
MAX_TEMP = 70
FAN_LOW = 40
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100



class NoctuaService:
 """Noctua fan controller service"""
 FAN_OFF = 0
 kill_now = False
 PI = None

 def __init__(self):
  self.PI = pigpio.pi()
  self.kill_now = False
  self.setFanSpeed(FAN_OFF)
  signal.signal(signal.SIGTERM,self.exit_gracefully)
  print("NoctuaService started")

 # Get CPU's temperature
 def getCpuTemperature(self):
  res = os.popen('vcgencmd measure_temp').readline()
  temp =(res.replace("temp=","").replace("'C\n",""))
  #print("temp is {0}".format(temp)) # Uncomment for testing
  return temp

 # Set fan speed
 def setFanSpeed(self,speed):
  dc= int(speed*10000)
  self.PI.hardware_PWM(FAN_PIN,PWM_FREQ,dc)
  return()

 # Handle fan speed
 def handleFanSpeed(self):
  temp = float(self.getCpuTemperature())
  # Turn off the fan if temperature is below MIN_TEMP
  if temp < MIN_TEMP:
   self.setFanSpeed(FAN_OFF)
   #print("Fan OFF") # Uncomment for testing
  # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
  elif temp > MAX_TEMP:
   self.setFanSpeed(FAN_MAX)
   #print("Fan MAX") # Uncomment for testing
  # Caculate dynamic fan speed
  else:
   step = (FAN_HIGH - FAN_LOW)/(MAX_TEMP - MIN_TEMP)
   temp -= MIN_TEMP
   #print(FAN_LOW + ( round(temp) * step )) # Uncomment for testing
   self.setFanSpeed(FAN_LOW + ( round(temp) * step ))
  return ()

 def exit_gracefully(self,signum,frame):
  self.setFanSpeed(FAN_HIGH)
  self.kill_now = True

 def run(self):
  try:
   while not self.kill_now:
    self.handleFanSpeed()
    time.sleep(WAIT_TIME)
  except  KeyboardInterrupt:
   self.kill_now =  True
  finally:
   self.setFanSpeed(FAN_HIGH)
   self.PI.stop()
   print("NoctuaService stopped")

if __name__ == '__main__':
 service = NoctuaService()
 service.run()

