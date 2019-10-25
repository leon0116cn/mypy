import random
import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta

USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/77.0.3865.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/73.0.3683.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) '
    'Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) '
    'Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
    'Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
    'Version/5.1 Safari/534.50',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; '
    '.NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'
]
DOMESTIC_FLIGHT_SEARCH_URL = "https://flights.ctrip.com/itinerary/api/12808/products"
DOMESTIC_FLIGHT_SEARCH_REFERER = "https://flights.ctrip.com/itinerary/oneway/sha-sia"
DOMESTIC_FLIGHT_SEARCH_TOKEN = '536bc24712ea27bb5109f78178533ba7'
REQUEST_TIMEOUT = 5


def get_domestic_flight_search_criteria(dcity='SHA', acity='SIA', days=20, **kwargs):
    airport_params = []
    qdate = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    airport_params.append({'dcity': dcity, 'acity': acity, 'date': qdate})
    search_criteria = {
        'flightWay': 'Oneway',
        'classType': 'ALL',
        'searchIndex': 1,
        'airportParams': airport_params,
        'token': DOMESTIC_FLIGHT_SEARCH_TOKEN
    }
    if 'airline' in kwargs:
        search_criteria['airline'] = kwargs['airline']
    if 'hasChild' in kwargs:
        search_criteria['hasChild'] = kwargs['hasChild']
    if 'hasBaby' in kwargs:
        search_criteria['hasBaby'] = kwargs['hasBaby']
    return search_criteria


def request_domestic_flight_search_criteria(search_criteria):
    if search_criteria:
        headers = {'user-agent': random.choice(USER_AGENT), 'referer': DOMESTIC_FLIGHT_SEARCH_REFERER}
        try:
            r = requests.post(DOMESTIC_FLIGHT_SEARCH_URL, headers=headers, json=search_criteria,
                              timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            show_request_params_detail(r)
            data = r.json()
            if data and data.get('msg') == 'success':
                return data
        except HTTPError as e:
            print('{0} requests error!'.format(r.url))
            print(e)


def parser_domestic_flight_json(json_data):
    flight_data = []
    for route in json_data.get('data').get('routeList'):
        if route.get('routeType') == 'Flight':
            leg = route.get('legs')[0]
            flight_id = leg.get('flightId')
            leg_type = leg.get('legType')

            # 航班价格信息
            characteristic = leg.get('characteristic')
            lowest_price = characteristic.get('lowestPrice')
            lowest_child_price = characteristic.get('lowestChildPrice')

            # 航班信息
            flight = leg.get('flight')
            airline_code = flight.get('airlineCode')
            airline_name = flight.get('airlineName')
            flight_number = flight.get('flightNumber')
            departure_date = flight.get('departureDate')
            arrival_date = flight.get('arrivalDate')
            punctuality_rate = flight.get('punctualityRate')
            craft_kind = flight.get('craftKind')
            craft_type_code = flight.get('craftTypeCode')
            craft_type_kind_display_name = flight.get('craftTypeKindDisplayName')
            craft_type_name = flight.get('craftTypeName')
            duration_days = flight.get('durationDays')
            fid = flight.get('id')
            meal_flag = flight.get('mealFlag')
            meal_type = flight.get('mealType')
            shared_flight_name = flight.get('sharedFlightName')
            shared_flight_number = flight.get('sharedFlightNumber')
            if shared_flight_name is not None:
                shared_flight = True
            else:
                shared_flight = False

            # 到达机场信息
            arrival_airport_info = leg.get('flight').get('arrivalAirportInfo')
            arrival_airport_name = arrival_airport_info.get('airportName')
            arrival_airport_tlc = arrival_airport_info.get('airportTlc')
            arrival_city_name = arrival_airport_info.get('cityName')
            arrival_city_tlc = arrival_airport_info.get('cityTlc')
            arrival_terminal_name = arrival_airport_info.get('terminal').get('name')
            arrival_terminal_id = arrival_airport_info.get('terminal').get('id')
            arrival_terminal_short_name = arrival_airport_info.get('terminal').get('shortName')

            # 起飞机场信息
            departure_airport_info = leg.get('flight').get('departureAirportInfo')
            departure_airport_name = departure_airport_info.get('airportName')
            departure_airport_tlc = departure_airport_info.get('airportTlc')
            departure_city_name = departure_airport_info.get('cityName')
            departure_city_tlc = departure_airport_info.get('cityTlc')
            departure_terminal_name = departure_airport_info.get('terminal').get('name')
            departure_terminal_id = departure_airport_info.get('terminal').get('id')
            departure_terminal_short_name = departure_airport_info.get('terminal').get('shortName')

            flight_data.append((airline_name, flight_number, lowest_price, departure_date, departure_airport_name,
                                departure_terminal_name, arrival_date, arrival_airport_name, arrival_terminal_name,
                                punctuality_rate, shared_flight_name, shared_flight_number, craft_type_name,
                                craft_type_kind_display_name, meal_flag))
    return flight_data


def get_domestic_flight_data():
    search_criteria = get_domestic_flight_search_criteria()
    json_data = request_domestic_flight_search_criteria(search_criteria)
    flight_data = parser_domestic_flight_json(json_data)
    return flight_data


def show_request_params_detail(r):
    if r:
        method = r.request.method
        if method == 'GET':
            print('*********' * 5)
            print('Request method is : {0}'.format(method))
            print('Request url is : {0}'.format(r.url))
            print('Request headers is {0}'.format(r.request.headers))
            print('*********' * 5)
        if method == 'POST':
            print('*********' * 5)
            print('Request method is : {0}'.format(method))
            print('Request url is : {0}'.format(r.url))
            print('Request body is {0}:'.format(r.request.body))
            print('Request headers is {0}'.format(r.request.headers))
            print('*********' * 5)


def main():
    print(get_domestic_flight_data())


if __name__ == '__main__':
    main()
