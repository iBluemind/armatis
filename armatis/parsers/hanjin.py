# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class HanjinParser(Parser):
    def __init__(self, invoice_number, config):
        super(HanjinParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://www.hanjin.co.kr/Delivery_html/inquiry' \
                                           '/result_waybill.jsp?wbl_num=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        tables = parser.find_all('tbody')

        if (len(tables) > 0):
            basic_info = tables[0].find_all('td', {'class': 'bb'})
            tracking_info = tables[1].find_all('tr')
            stuff_name = getattr(basic_info[1], 'get_text', '')(strip=True)
            sender_name = getattr(basic_info[3], 'get_text', '')(strip=True)
            receiver_name = getattr(basic_info[4], 'get_text', '')(strip=True)
            receiver_address = getattr(basic_info[5], 'get_text', '')(strip=True)

            parcel = Parcel()
            parcel.sender = sender_name
            parcel.receiver = receiver_name
            parcel.address = receiver_address
            parcel.note = stuff_name
            self.parcel = parcel

            for tr in tracking_info:
                tds = tr.find_all('td')
                if len(tds) == 5:
                    date = getattr(tds[0], 'get_text', '')(strip=True)
                    time = getattr(tds[1], 'get_text', '')(strip=True)
                    location = getattr(tds[2], 'get_text', '')(strip=True)
                    status = getattr(tds[3], 'get_text', '')(strip=True)
                    phone = getattr(tds[4], 'get_text', '')(strip=True)

                    track = Track()
                    track.time = '%s %s' % (date, time)
                    track.location = location
                    track.status = status
                    track.phone1 = phone
                    self.add_track(track)
