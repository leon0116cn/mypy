import random
from datetime import datetime, timedelta
import os
import requests
from requests.exceptions import HTTPError
import pandas as pd
import ctrip.settings as settings


def get_domestic_flight_search_criteria(dcity='SHA', acity='SIA', days=20, **kwargs):
    airport_params = []
    departure_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    airport_params.append({'dcity': dcity, 'acity': acity, 'date': departure_date})
    search_criteria = {
        'flightWay': 'Oneway',
        'classType': 'ALL',
        'searchIndex': 1,
        'airportParams': airport_params,
        'token': settings.DOMESTIC_FLIGHT_SEARCH_TOKEN
    }
    if 'airline' in kwargs:
        search_criteria['airline'] = kwargs['airline']
    if 'hasChild' in kwargs:
        search_criteria['hasChild'] = kwargs['hasChild']
    if 'hasBaby' in kwargs:
        search_criteria['hasBaby'] = kwargs['hasBaby']
    return search_criteria


def request_domestic_flight_search_criteria(search_criteria):
    try:
        headers = {'user-agent': random.choice(settings.USER_AGENT), 'referer': settings.DOMESTIC_FLIGHT_SEARCH_REFERER}
        r = requests.post(settings.DOMESTIC_FLIGHT_SEARCH_URL, headers=headers, json=search_criteria,
                          timeout=settings.REQUEST_TIMEOUT)
        r.raise_for_status()
        show_request_params_detail(r)
        data = r.json()
        if data and data.get('msg') == 'success':
            return data.get('data')
    except HTTPError as e:
        print('{0} requests error!'.format(r.url))
        print(e)


def parser_domestic_flight(data):
    if data:
        flight_data = []
        for route in data.get('routeList'):
            if route.get('routeType') == 'Flight':
                flight_item = dict(routeType=route.get('routeType'))

                #航班信息
                flight = route.get('legs')[0].get('flight')
                departureAirportInfo = parser_airport_info(flight.pop('departureAirportInfo'), 'departure')
                if departureAirportInfo:
                    flight.update(departureAirportInfo)
                arrivalAirportInfo = parser_airport_info(flight.pop('arrivalAirportInfo'), 'arrival')
                if arrivalAirportInfo:
                    flight.update(arrivalAirportInfo)
                flight_item.update(flight)

                #机票价格信息
                characteristic = route.get('legs')[0].get('characteristic')
                standardPrices = parser_standard_prices(characteristic.pop('standardPrices'))
                if standardPrices:
                    characteristic.update(standardPrices)
                flight_item.update(characteristic)

                flight_data.append(flight_item)

        return flight_data


def parser_airport_info(airport, flag):
    if airport:
        flaged_airport = {}
        for key, value in airport.items():
            if isinstance(value, dict):
                terminal = airport.get(key)
                for k, v in terminal.items():
                    flaged_airport['-'.join((flag, key, k))] = v
            else:
                flaged_airport['-'.join((flag, key))] = value
        return flaged_airport


def parser_standard_prices(standard_prices):
    prices = {}
    if standard_prices:
        for price in standard_prices:
            key = '-'.join((price['cabinClass'], 'cabinClass'))
            prices[key] = price['price']
        return prices


def get_domestic_flight_data():
    search_criteria = get_domestic_flight_search_criteria(days=10)
    data = request_domestic_flight_search_criteria(search_criteria)
    flight_data = parser_domestic_flight(data)
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


def export_domestic_flight(flight_data):
    df = pd.DataFrame(flight_data, columns=settings.DOMESTIC_FLIGHT_COLUMNS)
    df.columns = settings.DOMESTIC_FLIGHT_DF_COLUMNS
    now = datetime.now().strftime('%Y-%m-%d')
    file_name = os.path.join(settings.EXPORT_FILE_PATH, '{0}.xlsx'.format(now))
    df.to_excel(file_name, index=False)


def main():
    flight_data = get_domestic_flight_data()
    export_domestic_flight(flight_data)


if __name__ == '__main__':
    main()
