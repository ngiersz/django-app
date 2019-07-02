import requests


class Geocoder:

    def __init__(self):
        self.access_token = 'pk.eyJ1IjoibmdpZXJzeiIsImEiOiJjanhrb25vZGowM3ppM3lvdTF5dndweDRvIn0.bWhpnTDM-vbSB2p9XD0JPg'
        self.base_mapbox_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places'

    # {base_mapbox_url}/{address}.json?access_token={access_token}
    def getUrlForGeocoding(self, address):
        return self.base_mapbox_url + '/' + str(address) + '.json?access_token=' + self.access_token

    def getLngLat(self, address):
        response = requests.get(self.getUrlForGeocoding(address))
        return response.json().get('features')[0].get('center')


if __name__=='__main__':
    geocoding = Geocoder()

    address = 'Byszewska 19/2, Bydgoszcz, Poland'
    street = address.split('/')[0]
    city_and_country = address.split('/')[1].split(',', 1)[1]
    formatted_address = street + ',' + city_and_country
    lng_lat_1 = geocoding.getLngLat(formatted_address)
    print(lng_lat_1)
    # print(geocoding.getLngLat('Poznań, Poland'))
