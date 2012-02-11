# HToTel2
## What is this all about ?
This is a stupid simple HTTP over Telnet over Telnet forwarder.

## Known issues

* So far this only works for Cisco Switches with a users login ( ">" prompt)
* Does not work with images ... (And no clue why)

## Getting started

Here is a "real-life" scenario :

* You have access to your company gateway router using telnet
* You want to access internal webserver from outside without using NAT 


### Let's give it a try :

```$ python HToTel2.py  your.public.ip.addr telnet_password some.internal.server
```

Open up a browser and browse to :
http://locahost:23238

Enjoy.

All fixes and improvements are really welcome, I'm still a beginner in Python.