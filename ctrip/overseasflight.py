import hashlib
import json
import random
import re
from datetime import datetime, timedelta
import requests
from requests.exceptions import HTTPError

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
SEARCH_CRITERIA_URL = 'https://flights.ctrip.com/international/search/'
OVERSEAS_FLIGHT_SEARCH_URL = 'https://flights.ctrip.com/international/search/api/search/batchSearch'
REQUEST_TIMEOUT = 5


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


def regex_overseas_flight_search_criteria(html_doc):
    pattern = re.compile('GlobalSearchCriteria =(.*);')
    results = re.search(pattern, html_doc)
    if results:
        return results.group(1)


def generate_overseas_flight_sign(post_data):
    if post_data:
        tran_id = post_data.get('transactionID')
        dcity_code = post_data.get('flightSegments')[0].get('departureCityCode')
        acity_code = post_data.get('flightSegments')[0].get('arrivalCityCode')
        depdate = post_data.get('flightSegments')[0].get('departureDate')
        md5 = hashlib.md5()
        encode_str = ''.join((tran_id, dcity_code, acity_code, depdate))
        md5.update(encode_str.encode('utf-8'))
        return md5.hexdigest()


def get_overseas_flight_search_criteria(dcity='SHA', acity='TYO', days=20, direct_flight=1):
    headers = {'user-agent': random.choice(USER_AGENT)}
    postfix = '-'.join(['oneway', dcity, acity])
    url = SEARCH_CRITERIA_URL + postfix
    dep_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'depdate': dep_date, 'cabin': 'y_s', 'adult': 1, 'child': 0, 'infant': 0, 'directflight': direct_flight}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        show_request_params_detail(r)
        search_criteria = json.loads(regex_overseas_flight_search_criteria(r.text))
        return search_criteria
    except HTTPError as e:
        print('{0} requests error!'.format(r.url))
        print(e)


def request_overseas_flight_search_criteria(search_criteria):
    if search_criteria:
        sign = generate_overseas_flight_sign(search_criteria)
        tran_id = search_criteria.get('transactionID')
        headers = {'user-agent': random.choice(USER_AGENT), 'transactionid': tran_id, 'sign': sign}
        try:
            r = requests.post(OVERSEAS_FLIGHT_SEARCH_URL, headers=headers, json=search_criteria,
                              timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            show_request_params_detail(r)
            json_data = r.json()
            if json_data and json_data.get('msg') == 'success':
                return json_data
        except HTTPError as e:
            print('{0} requests error!'.format(r.url))
            print(e)


def parser_overseas_flight_json(json_data):
    flight_data = []
    for flight_itinerary in json_data.get('data').get('flightItineraryList'):
        itinerary_id = flight_itinerary.get('itineraryId')

        #航段信息
        flight_segment = flight_itinerary.get('flightSegments')[0]
        airline_code = flight_segment.get('airlineCode')
        airline_name = flight_segment.get('airlineName')
        cross_days = flight_segment.get('crossDays')
        duration = flight_segment.get('duration')
        transfer_count = flight_segment.get('transferCount')
        stop_count = flight_segment.get('stopCount')
        segment_no = flight_segment.get('segmentNo')

        #航班信息
        flight = flight_segment.get('flightList')[0]
        flight_no = flight.get('flightNo')
        airline_code = flight.get('marketAirlineCode')
        airline_name = flight.get('marketAirlineName')
        alliance = flight.get('marketAlliance')
        airline_duration = flight.get('duration')
        departure_date = flight.get('departureDateTime')
        arrival_date = flight.get('arrivalDateTime')
        aircraft_code = flight.get('aircraftCode')
        aircraft_name = flight.get('aircraftName')
        aircraft_size = flight.get('aircraftSize')

        #起飞机场信息
        dairport_code = flight.get('departureAirportCode')
        dairport_name = flight.get('departureAirportName')
        dairport_short_name = flight.get('departureAirportShortName')
        dcity_code = flight.get('departureCityCode')
        dcity_id = flight.get('departureCityId')
        dcity_name = flight.get('departureCityName')
        dcountry_name = flight.get('departureCountryName')
        dprovince_id = flight.get('departureProvinceId')
        departure_terminal = flight.get('departureTerminal')

        #到达机场信息
        aairport_code = flight.get('arrivalAirportCode')
        aairport_name = flight.get('arrivalAirportName')
        aairport_short_name = flight.get('arrivalAirportShortName')
        acity_code = flight.get('arrivalCityCode')
        acity_id = flight.get('arrivalCityId')
        acity_name = flight.get('arrivalCityName')
        acountry_name = flight.get('arrivalCountryName')
        aprovince_id = flight.get('arrivalProvinceId')
        arrival_terminal = flight.get('arrivalTerminal')

        #价格信息
        prices = flight_itinerary.get('priceList')[0]
        adult_price = prices.get('adultPrice')
        adult_tax = prices.get('adultTax')
        cabin = prices.get('cabin')

        flight_data.append((airline_name, flight_no, adult_price, adult_tax, duration, cross_days, departure_date,
                            dcountry_name, dcity_name, dairport_name, departure_terminal, arrival_date, acountry_name,
                            acity_name, aairport_name, arrival_terminal, aircraft_name))
    return flight_data


def get_overseas_flight_data():
    search_criteria = get_overseas_flight_search_criteria()
    json_data = request_overseas_flight_search_criteria(search_criteria)
    flight_data = parser_overseas_flight_json(json_data)
    return flight_data


def main():
    print(get_overseas_flight_data())


if __name__ == '__main__':
    main()

