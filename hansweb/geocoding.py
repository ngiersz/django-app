import requests


class Geocoder:

    def __init__(self):
        self.access_token = 'pk.eyJ1IjoibmdpZXJzeiIsImEiOiJjanhrb25vZGowM3ppM3lvdTF5dndweDRvIn0.bWhpnTDM-vbSB2p9XD0JPg'
        self.base_mapbox_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places'

    # {base_mapbox_url}/{address}.json?access_token={access_token}
    def get_url_for_geocoding(self, address):
        return f'{self.base_mapbox_url}/{address}.json?access_token={self.access_token}'

    def get_lng_lat(self, address):
        response = requests.get(self.get_url_for_geocoding(address))
        return response.json().get('features')[0].get('center')

