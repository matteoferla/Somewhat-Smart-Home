# Set-up

This is mostly a collection of code I copy paste a lot.

## Connection

Make SSH on freshly flashed

    touch /Volumes/boot/ssh
    
WIFI supplicant code:

    nano /Volumes/boot/wpa_supplicant.conf
    
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=GB
    
    network={
     ssid="👾👾👾👾"
     psk="👾👾👾👾"
    }
    
## First steps

First ssh:

    passwd
    echo "source ~/.bashrc" >>  ~/.bash_profile
    echo "source ~/.profile" >>  ~/.bash_profile

    sudo apt update && sudo apt upgrade -y

Git:

    sudo apt-get -y install git
    
Using system python3, namely `/usr/bin/python3` as opposed to berryconda:

    sudo apt-get -y install python3-pandas
    sudo apt-get -y  install python3-dev
    sudo apt-get -y  install python3-pip
    sudo apt-get -y install python3-sqlalchemy
    sudo pip3 install jupyter RPi.GPIO waitress flask Flask-Ask Flask-SQLAlchemy beautifulsoup4 Pillow picamera adafruit-circuitpython-dht adafruit-blinka

Berryconda is good, but is limited to 3.6 max and does not allow SD card switching between arm6 and arm7 (`Illegal operation`).

## Jupyter

### Tweak jupyter

Make sure Jupyter is installed —previous block. Add password:

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
Give the path of jupyter:

* If jupyter was installed with sudo: `/usr/local/bin/`
* If jupyter was installed without sudo: `/home/pi/.local/bin/jupyter`
* If jupyter was installed with berryconda: `/home/pi/berryconda3/???/jupyter`

and then:

    echo '#!/bin/bash\n/home/pi/.local/bin/jupyter notebook --no-browser --ip="*"' > run_jupyter.sh 
    sudo systemctl start jupyter
    sudo systemctl enable jupyter
    
If stuff does not work (generally filename wrong etc.)
    
    sudo systemctl status jupyter

Or 

    sudo journalctl -u jupyter

## Slack

The above is fine, but it is nice to know who is who:

    #!/bin/bash
    PI_NAME='👾👾👾'
    SLACKHOOK="https://hooks.slack.com/services/👾👾👾/👾👾👾/👾👾👾"
    while true
    do
    echo 'reporting...'
    HOST_IP=$(hostname -I)
    PAYLOADSLACK='{"text":"$PI_NAME '$HOST_IP'"}'
    curl -X POST -H 'Content-type: application/json' --data "$PAYLOADSLACK" $SLACKHOOK
    if [ $? -eq 0 ]
    then
    break
    fi
    sleep 1
    done
    
    /usr/bin/jupyter  notebook --no-browser --ip="*"

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

