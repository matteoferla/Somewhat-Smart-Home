# Furbexa

The idea and the majority of the setup came form [a blog post](https://howchoo.com/g/otewzwmwnzb/amazon-echo-furby-using-raspberry-pi-furlexa)
However, there were lots of problems and differences.

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

Parts I have added:

* Pi Zero W
* 4x rechargeable AA (each 1.3V)

## Tests

Some suggestions to test for second hand Furbies off the web sold as is...

* test mouth button —ears, eyelids and cycle trigger
* test speaker
* test motor (5V is fine)
* test battery unit

Mine had a dodgy battery unit (rusty and broken connector).

## Pi

So I really struggled to pack a Pi Zero between the body and the battery unit.
Regular header pins fit but not with wires on them (I was using chunky 18 gauge).
I failed to solder wires on the board without them coming off etc.
So I opted for the two row angle header pins with a gap.

The shim + microphone does not fit in. So two things were tried:

* Adafruit's DIY USB parts —the micro-USB is too long
* PP1 + PP6 wired to a female breakout board

## Standard stuff
### SSH and update

* Added `ssh` file to boot drive before ejecting it from computer.
* SSHed using default user `pi` and password `raspberry`

set password to something else

    sudo passwd
    echo "source ~/.bashrc" >>  ~/.bash_profile
    echo "source ~/.profile" >>  ~/.bash_profile
    sudo apt update && sudo apt upgrade -y
    
Adding to `.bash_profile`:
    
    export PATH=$PATH:/home/pi/.local/bin

### Python

    sudo apt-get -y install python3-pandas
    sudo apt-get -y  install python3-dev
    sudo apt-get -y  install python3-pip  
    sudo pip3 install jupyter RPi.GPIO waitress flask Flask-Ask Flask-SQLAlchemy beautifulsoup4 Pillow picamera
    
### Jupyter

As discussed elsewhere

    nano run_jupyter.sh
    sudo nano /etc/systemd/system/jupyter.service
    jupyter notebook password
    sudo systemctl start jupyter
    sudo systemctl enable jupyter
    
### WiFi

    sudo raspi-config 

Setting network and hostname to `furby`.

## Speaker

> Amazon no longer allows AlexaPi & co. to pay music. 
> And there's a fur coat in between and a motor to compete with so sound quality is not a must.

* 5V
* GPIO13 (mono)
* native 32Ω speaker

The original tutorial speaks of the speaker being poor.
In mine it's not that bad and actually better than two 8Ω 1W speakers in loudness, so I am sticking with it.
It still needs an Amp, using a PAM8302A audio amp wiring V<sub>CC</sub> to 5V (tinny, but loud).
That is with `alsamixer` set to max and the variable resistor left as is.

Audio-in with a 10 nF ceramic cap (manually determined) to gnd can stop the tinniness, but lowers volume.

The best explanation of the PWM audio I found is https://librpip.frasersdev.net/peripheral-config/pwm0and1/
To configure PWM audio add to `/boot/config.txt`, but first copy it:

    mkdir backup
    cp /boot/config.txt backup/boot_config.txt

Then adding —for discussion about `func` see https://sudomod.com/forum/viewtopic.php?t=480&start=30

    dtoverlay=pwm,pin=13,func=2

To it and restarting    

    sudo nano /boot/config.txt 
    sudo shutdown -r now

Here are some commands:
    
* list speakers: `aplay -l`
* volume control: `alsamixer`
* play loop: `speaker-test -t wav -c 1`
* play once: `aplay /usr/share/sounds/alsa/Front_Center.wav`

The following were installed in first SD card but not in second (?)

    sudo apt-get -y install  git gcc cmake build-essential libsqlite3-dev libcurl4-openssl-dev libfaad-dev libssl-dev libsoup2.4-dev libgcrypt20-dev libgstreamer-plugins-bad1.0-dev  gstreamer1.0-plugins-good libasound2-dev doxygen
    cd /home/pi/sdk-folder/third-party
    wget -c http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz


## Alexa

This differs from the tutorial and is more straightforward.

Using AlexaPi: https://github.com/alexa-pi/AlexaPi/wiki/Installation

This will install via pip3 `backports.functools-lru-cache, certifi, more-itertools, cheroot, pytz, jaraco.functools, tempora, portend, zc.lockfile, cherrypy, humanfriendly, coloredlogs, idna, pocketsphinx, pyaudio, python-vlc, pyyaml, urllib3, requests, webrtcvad`

    sudo apt-get install git
    cd /opt
    sudo git clone https://github.com/alexa-pi/AlexaPi.git
    sudo ./AlexaPi/src/scripts/setup.sh

This will require a few keys to be generated via the Amazon dev site:

* Amazon ID: `👾👾👾`
* Product Name: `Furbexa`
* Product ID: `Furbexa`
* Amazon ID: `👾👾👾`
* Security Profile: `Furbexa`
* Security Profile ID: `amzn1.application.👾👾👾`
* Client ID: `amzn1.application-oa2-client.👾👾👾`
* Client Secret: `👾👾👾`

Also, the permissions IP within the network (192.168.1.xx) are important as the Pi is headless.

The refresh token comes from `/usr/bin/python3 /opt/AlexaPi/src/auth_web.py` run as root.
Which is required by `/usr/bin/python3 /opt/AlexaPi/src/main.py`.
Which is run by the alexapi service, which is present in `/usr/lib/systemd/system/AlexaPi.service`.

Changing

    sudo nano /etc/opt/AlexaPi/config.yaml
    
* GPIO18 --> sensor for mouth (this is a pull-up input (positive), not negative!)
* GPIO24 --> green light
* GPIO14 --> red light

## Mouth sensor and forehead

The month sensor (white) wires were not too sturdy and came off easily.
So if I were to repeat this I would solder 22 gaugewires from the get go.

There is are also two mysterious wires, which I have no idea what they do.
The internet isn't helpful.

I removed the internal board on the forehead, added a small green and a red LED and an unconnected photoresistor.
The LEDs work well even with the tinted cover.
The photoresistor is just for aesthetics as reading it would be a pain.

Pin test:

    import board, digitalio, time
    
    for color, pin in {'green': board.D24, 'red': board.D14}.items():
        print(color)
        with digitalio.DigitalInOut(pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            led.value = True
            time.sleep(2)
            led.value = False
            
Test buttons:

    with digitalio.DigitalInOut(board.D18) as switch:
        switch.direction = digitalio.Direction.INPUT
        switch.pull = digitalio.Pull.UP
        print('pressed' if not switch.value else 'unpressed')


## Motor

I debated using just a rectifier as opposed to TB6612 (as it's overkill), 
but a driver has the advantage of being able to go backwards (H-bridge business).
There is a motor cycle sensor on the Furby, so going backwards would be essential to make it chuckle etc.

* https://learn.adafruit.com/adafruit-tb6612-h-bridge-dc-stepper-motor-driver-breakout/pinouts
* https://github.com/Howchoo/random-bits/blob/master/furlexa-echo-furby/pi-furby-dc-motor-TB6612-pi_bb.png

motion sensing as on original discussion. Namely if there is a sound playing it moves.

    /home/pi/furby/output-monitor.sh
    /etc/init.d/go-furby-go.sh start
    
This is not great.

NB. AIN1 comes after AIN2 on the TB6612

Here is some test code:

    GPIO.output(27, GPIO.HIGH) # Set AIN1 
    GPIO.output(17, GPIO.LOW) # Set AIN2

Set the motor speed

    GPIO.output(7, GPIO.HIGH) # Set PWMA

Disable STBY (standby)

    GPIO.output(4, GPIO.HIGH)

### Sound <-> Motor
 Signal out of the Amp isn't strong enough to trigger movement.
Plus, signal from PWM, even at low frequencies, just results in a slow movement, not a jerky one.
So one would need to have an intensity based cutoff to make it jerky.
However, there is no space to add custom circuitry like bandpass filters etc.
The very minimum would be a GPIO13 -> resistor -> PNP transistor base -> TB6612 and that is already too much.


## USB Microphone

* list mikes: `arecord -l`
* test mikes: `arecord -D plughw:1,0 -d 3 test.wav && aplay test.wav`