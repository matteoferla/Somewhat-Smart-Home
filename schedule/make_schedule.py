from mako.template import Template

template = Template(filename='scheduled_tasks.py.mako')

rendered = template.render(pi_name='👾👾👾',
                          ip='👾👾👾',
                          pi_description='👾👾👾',
                          gateway='👾👾👾',
                          key='👾👾👾',
                          sensors={'DS18S20': None,
                                   'DHT22': 17}
                          )

print(rendered)