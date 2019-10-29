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
REQUEST_TIMEOUT = 5
DOMESTIC_FLIGHT_SEARCH_URL = "https://flights.ctrip.com/itinerary/api/12808/products"
DOMESTIC_FLIGHT_SEARCH_REFERER = "https://flights.ctrip.com/itinerary/oneway/sha-sia"
DOMESTIC_FLIGHT_SEARCH_TOKEN = '536bc24712ea27bb5109f78178533ba7'
DOMESTIC_FLIGHT_COLUMNS = ['flightNumber', 'airlineName', 'sharedFlightNumber', 'sharedFlightName', 'departureDate',
                           'arrivalDate', 'punctualityRate', 'departure-cityName', 'departure-cityTlc',
                           'departure-airportName', 'departure-airportTlc', 'departure-terminal-name',
                           'arrival-cityName', 'arrival-cityTlc', 'arrival-airportName', 'arrival-airportTlc',
                           'arrival-terminal-name', 'craftTypeName', 'craftKind', 'lowestPrice', 'lowestChildPrice',
                           'Y-cabinClass', 'C-cabinClass', 'F-cabinClass', 'tax', 'mealType']
DOMESTIC_FLIGHT_DF_COLUMNS = ['Fn', 'Airline', 'Shared-Fn', 'Shared-Airline', 'Dept-Date', 'Arri-Date', 'Pun-Rate',
                              'Dept-City', 'Dept-CityTlc', 'Dept-Airport', 'Dept-AirportTlc', 'Dept-Terminal',
                              'Arri-City', 'Arri-CityTlc', 'Arri-Airport', 'Arri-AirportTlc', 'Arri-Terminal', 'Craft',
                              'CraftKind', 'L-Price', 'LC-Price', 'Tax', 'Meal']
EXPORT_FILE_PATH = 'E:\\MyProjects\\Pycharm\\mypy\\data\\'
