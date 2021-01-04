def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('status', '/status')
    config.add_route('read', '/read')
    config.add_route('show', '/show')
    config.add_route('delete', '/delete')
    config.add_route('night', '/night')
    config.add_route('record', '/record') # add measurement  --> .models.Measurement
    config.add_route('store', '/store') # add photo  --> .models.Photo
    config.add_route('define', '/define') # add details of sensor  --> .models.Details