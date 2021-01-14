## Scheduled recordings

In each sensor pi, I have a system daemon service controlled python script,
which uses the advanced python scheduler to take a measurement.

However, each sensor pi has something different.

## Service

Add [service](scheduled.service):

    sudo nano /etc/systemd/system/scheduled.service

Which will run ``scheduled_tasks.py``, which can be generated from templates...

    from mako.template import Template
    from mako.lookup import TemplateLookup
    
    mylookup = TemplateLookup(directories=['.'])
    template = Template(filename='scheduled_tasks.py.mako', lookup=mylookup)
    
    rendered = template.render(pi_name='👾👾👾',
                              ip='👾👾👾',
                              pi_description='👾👾👾',
                              gateway='👾👾👾',
                              key='👾👾👾',
                              sensors={'DS18S20': None,
                                       'DHT22': 17}
                              )
    
    print(rendered)
    
    with open('👾👾👾.py', 'w') as w:
        w.write(rendered)