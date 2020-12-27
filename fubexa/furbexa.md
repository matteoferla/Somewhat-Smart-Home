# Furbexa

The idea and the majority of the setup came form [a blog post](https://howchoo.com/g/otewzwmwnzb/amazon-echo-furby-using-raspberry-pi-furlexa)

## Hardware

The Furby has

* a 32Ω 0.25W speaker
* a mouth button
* a chest button (on the speaker)
* a back button
* an "inversion sensor" on the board &larr; gyroscope
* mystery something next to mouth
* a motor, which runs slower between 2.5V-3.0V, at 5V it smells like copper
* a full revolution trigger
* small LED
* big LED
* photoresistor

### Speaker

The original tutorial speaks of the speaker being poor.
In mine it's not that bad and actually better than two 8Ω speakers in loudness, so I am sticking with it.
It still needs an Amp, using a PAM8302A audio amp wiring V<sub>CC</sub> to 5V (tinny, but loud).

## Software
