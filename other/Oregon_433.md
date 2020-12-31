## Oregon scientific sensors

I have two Oregon scientific sensors (THN132N) and a BAR266 display thinggy.
I was given these for Christmas some time back and I have not really managed to intercept the signal to log them.

There are a few different libraries to do things. In Python, the best seems:

    sudo pip3 install rpi-rf

However, it does not seem to intercept the signals from the sensors:

    import signal
    import sys
    import time
    import logging
    
    from rpi_rf import RFDevice
    receiving_pin = 27
    rfdevice = RFDevice(receiving_pin)
    rfdevice.enable_rx()
    
    # sniff
    timestamp = None
    rfdevice.rx_pulselength
    signals = []
    while True:
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            signal = {key: getattr(rfdevice, 'rx_'+key) for key in ('code', 'pulselength', 'proto','bitlength', 'tolerance', 'code_timestamp')}
            signal['time'] = datetime.datetime.now()
            print(signal)
            signals.append(signal)
    rfdevice.cleanup()
    
After interrupting it:
    
    import pandas as pd

    pd.DataFrame(signals)
    
I see it blink it's LED... but nada.
There is also `GNURadio` however apt-get installs in python 2.7. So I really don't want that.

The Oregon sensor is documented in a (pdf)[http://wmrx00.sourceforge.net/Arduino/OregonScientific-RF-Protocols.pdf).
And there are (C scripts for it)[https://github.com/merbanan/rtl_433/blob/ea797cff8cafd7fc385f8cf413f072df725f9e5e/src/devices/oregon_scientific.c].

My guess is that the pulsetime is too short for the Pi to work, so I need to use an arduino, which requires more effort, so I have not tried.

   
   
