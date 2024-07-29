from Request.Condor import Condor
from File.FileManager import FileManager

class RouteManager:

    def __init__(self, routes):
        for route in routes:
            condor = Condor(route['origin'], route['destination'], route['oneway'])
            file_manager = condor.create_file_manager()
            file_manager.write_file(condor.execute_request())
                

routes = [
    {'origin': 'WRO', 'destination': 'PUJ', 'oneway': False},
    {'origin': 'WRO', 'destination': 'PUJ', 'oneway': True},
    {'origin': 'PUJ', 'destination': 'WRO', 'oneway': True},
    {'origin': 'WAW', 'destination': 'PUJ', 'oneway': False},
    {'origin': 'WAW', 'destination': 'PUJ', 'oneway': True},
    {'origin': 'PUJ', 'destination': 'WAW', 'oneway': True},
    {'origin': 'KRK', 'destination': 'PUJ', 'oneway': False},
    {'origin': 'KRK', 'destination': 'PUJ', 'oneway': True},
    {'origin': 'PUJ', 'destination': 'KRK', 'oneway': True},
    {'origin': 'FRA', 'destination': 'PUJ', 'oneway': False},
    {'origin': 'FRA', 'destination': 'PUJ', 'oneway': True},
    {'origin': 'PUJ', 'destination': 'FRA', 'oneway': True},
    {'origin': 'DRS', 'destination': 'PUJ', 'oneway': False},
    {'origin': 'DRS', 'destination': 'PUJ', 'oneway': True},
    {'origin': 'PUJ', 'destination': 'DRS', 'oneway': True},

]

route_manager = RouteManager(routes)