import random
import requests
from requests.exceptions import HTTPError


CTRIP_POI_URL = "https://flights.ctrip.com/itinerary/api/poi/get"
REQUESTS_TIMEOUT = 10
USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'
]
POST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
}
POI_LABEL = ['pn', 'fn', 'sn', 'snc', 'cate', 'cn']


def get_flight_poi():
    try:
        POST_HEADERS['user-agent'] = random.choice(USER_AGENT)
        r = requests.get(CTRIP_POI_URL, headers=POST_HEADERS, timeout=REQUESTS_TIMEOUT)
        r.raise_for_status()
        poi_json_data = r.json()
        if poi_json_data and poi_json_data.get('msg') == 'success':
            return poi_json_data.get('data')
    except HTTPError as e:
        print('{0} requests ERROR!'.format(CTRIP_POI_URL))
        print(e)


def parser_flight_poi(json_data, poi_data):
    for key1, item_first in json_data.items():
        if isinstance(item_first, dict):
            for key2, item_second in item_first.items():
                for item in item_second:
                    poi_item = item.get('data').split('|')
                    poi_item.append(key1)
                    poi_item.append(item.get('display'))
                    poi_data.append(dict(zip(POI_LABEL, poi_item)))
        elif isinstance(item_first, list):
            for item in item_first:
                poi_item = item.get('data').split('|')
                poi_item.append(key1)
                poi_item.append(item.get('display'))
                poi_data.append(dict(zip(POI_LABEL, poi_item)))


def print_flight_poi(poi_data):
    print(poi_data)


def main():
    poi_data = []
    json_data = get_flight_poi()
    parser_flight_poi(json_data, poi_data)
    print_flight_poi(poi_data)


if __name__ == '__main__':
    main()