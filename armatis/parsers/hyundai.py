# -*- coding: utf-8 -*-


from armatis.models import Parcel, Track
from armatis.parser import Parser, ParserRequest


EMPTY_TEXT = 'null'


class HyundaiParser(Parser):
    def __init__(self, invoice_number):
        super(HyundaiParser, self).__init__(invoice_number)
        parser_request = ParserRequest()
        parser_request.url = 'http://www.hlc.co.kr/hydex/jsp/tracking' \
                             '/trackingViewCus.jsp?InvNo=%s' % self.invoice_number
        self.parser_request = parser_request

    def parse(self, parser, response):
        td = parser.find_all('td', {'style': 'padding:0 0 0 10'})

        sender_name = td[0].get_text(strip=True)
        receiver_name = td[2].get_text(strip=True)
        address = td[3].get_text(strip=True)

        parcel = Parcel()
        if sender_name is not EMPTY_TEXT:
            parcel.sender = sender_name
        if receiver_name is not EMPTY_TEXT:
            parcel.receiver = receiver_name
        if address is not EMPTY_TEXT:
            parcel.address = address
        self.parcel = parcel

        dates = parser.find_all('td', {'width': '102', 'height': '28', 'align': 'center'})
        times = parser.find_all('td', {'width': '67', 'align': 'center'})
        places = parser.find_all('td', {'width': '108', 'align': 'center'})
        messages = parser.find_all('td', {'width': '277', 'style': 'padding:0 0 0 5'})

        for index, date in enumerate(dates):
            time = getattr(date, 'get_text', '')(strip=True) + ' ' + getattr(times[index], 'get_text', '')(strip=True)
            location = getattr(places[index], 'get_text', '')(strip=True)
            status = getattr(messages[index], 'get_text', '')(strip=True)

            track = Track()
            track.time = time
            track.location = location
            track.status = status
            self.add_track(track)

