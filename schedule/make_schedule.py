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
