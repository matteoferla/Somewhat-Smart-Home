# Set-up

This is mostly a collection of code I copy paste a lot.

## Connection

Make SSH on freshly flashed

    touch /Volumes/boot/ssh
    
TODO ADD WIFI supplicant code.
    
## First steps

First ssh:

    passwd
    echo "source ~/.bashrc" >>  ~/.bash_profile
    echo "source ~/.profile" >>  ~/.bash_profile

    sudo apt update && sudo apt upgrade -y

Using system python3, namely `/usr/bin/python3` as opposed to berryconda:

    sudo apt-get -y install python3-pandas
    sudo apt-get -y  install python3-dev
    sudo apt-get -y  install python3-pip
    sudo apt-get -y install python3-sqlalchemy
    pip3 install jupyter RPi.GPIO waitress flask Flask-Ask Flask-SQLAlchemy beautifulsoup4 Pillow picamera adafruit-circuitpython-dht adafruit-blinka

Git:

    sudo apt-get install git

## Jupyter

### Install jupyter

Make sure/install Jupyter

    sudo apt-get -y  install python3-pandas
    sudo apt-get -y  install python3-dev
    sudo apt-get -y install python3-pip
    jupyter notebook password
    
Having the same theme of a notebook as another one can be confusing

    pip3 install jupyter jupyterthemes
    jt -N -T -t grade3

To list themes:

    jt -l
    
I put screenshot of these on [my blog](http://blog.matteoferla.com/2020/11/remote-notebooks-and-jupyter-themes.html).


### Jupyer service

Making a service:

    sudo nano /etc/systemd/system/jupyter.service

Adding something like:

    [Unit]
    Description=Run jupyer notebook
    After=network.target
    
    [Service]
    User=pi
    WorkingDirectory=/home/pi/
    ExecStart=bash /home/pi/run_jupyter.sh
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
   
Don't be fancy with sudo printf or echo.
Assuming jupyter is in `/home/pi/.local/bin/jupyter` and then:
    
    echo '#!/bin/bash\n/home/pi/.local/bin/jupyter notebook --no-browser --ip="*"' > run_jupyter.sh 
    sudo systemctl start jupyter
    sudo systemctl status jupyter
    sudo systemctl enable jupyter
    
If stuff does not work (generally filename wrong etc.)

    sudo journalctl -u jupyter
## Pins

Show in a Jupyter notebook cell what the pins are:

    from IPython.display import display, HTML
    import RPi.GPIO as GPIO
    import time
    # for GPIO numbering, choose BCM
    GPIO.setmode(GPIO.BCM)

    display(HTML(
        '<img width="50%" src="https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png"/>'))


## Testing the soldering

It's totally not needed when the soldering is good,
but sometimes one is forced to use something other than headers.
    
    pin = 21
    
    GPIO.setup(pin, GPIO.OUT)
    for i in range(5):
        print(i)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)
    
    GPIO.output(pin, GPIO.LOW)

