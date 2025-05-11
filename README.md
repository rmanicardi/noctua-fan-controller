# noctua-fan-controller


Inspired by https://blog.driftking.tw/en/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/ this version has the goal to solve the issue of wobbling speed due to software PWM used by the RPI GPIO library.

The code has been rewritten to use pigpio and the systemd service has been written to consider dependencies to this library and handle of the correct service termination.



Since it depends on pigpio:

--- 
Installation on ubuntu/debian

install the dependency through

apt-get install pigpio



---
 Installation on Batocera:

  Batocera does not comes with systemd so you'll need to use the native service system (for more info see https://wiki.batocera.org/scripting_services_rules_examples)

 - pigpio is already installed 
 - copy all the files from this repo in /userdata/system/noctua
 - copy the service file from ./batocera-services to /userdata/system/services
 - run 'batocera-services enable noctua'
 - From Batocera EmulationStation frontend go to MAIN MENU->SYSTEM SETTINGS->SERVICE and enable the 'pigpio' (first) and the the 'noctua' (last) services

 Note: in this version there is the file 'pigpio.py' which I've copied from the python3-pigpio package. This is not provided by Batocera