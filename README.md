# noctua-fan-controller


Inspired by https://blog.driftking.tw/en/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/ this version has 
the goal to solve the issue of wobbling speed due to software PWM used by the RPI GPIO library.

The code has been rewritten to use pigpio and the systemd service has been written to consider dependencies to this library and 
handle of the correct service termination.

Since it depends on pigpio, install it through

apt-get install pigpio
