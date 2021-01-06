# Somewhat-Smart-Home
Integrating the Raspberry pi across the house!

This repo contains several projects and supercedes others:

* [https://github.com/matteoferla/Temperature-moniting-website-via-Rasberry-Pi](https://github.com/matteoferla/Temperature-moniting-website-via-Rasberry-Pi)
* [https://github.com/matteoferla/Raspberry-Pi-irrigator](https://github.com/matteoferla/Raspberry-Pi-irrigator) —actually the latter still contains a lot of useful info

## Set-up

> See [setup](setting_up.md)

There are a few things I do on every Pi:

* Make a file saying who the Pi is
* Install Jupyter notebook and make it run at start-up
* Slack message of it's IP address
* etc.

## Furbexa

> TODO move data over and collect photos

## Homesensing

> TODO this project is not up yet

This has two parts.

* Miscellaneous Raspberry Pis across the house with different sensors
* A webserver Raspberry Pi (Pi 2) that receives the measurements and serves them

## Webservers


> TODO See LINK TO REPOS

My main webservers are actually on a different Pi namely, a Pi 4.
However, I do not want to stress too much even if it's 4 GB.
Furthermore, I do not want to use the GPIO (well, bar for the fan as it gets rather hot)
because shorting will reset the Pi and Ubuntu x64 is a pain with the GPIO.




