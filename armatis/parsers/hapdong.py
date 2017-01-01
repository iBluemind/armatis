# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class HapdongParser(Parser):
    def __init__(self, invoice_number, config):
        super(HapdongParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://www.hdexp.co.kr/parcel' \
                                           '/order_result_t.asp?p_item=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        tables = parser.find_all('table', {'class': 'order_tb_result'})

        tds = tables[0].find_all('td')
        sender = getattr(tds[9], 'string', '')
        receiver = getattr(tds[11], 'string', '')
        address = getattr(tds[19], 'string', '')

        tr = tables[1].find_all('tr')[1]
        memo = getattr(tr.find_all('td')[3], 'string', '') + ' ' + getattr(tr.find_all('td')[4], 'string', '')

        parcel = Parcel()
        parcel.sender = sender
        parcel.receiver = receiver
        parcel.address = address
        parcel.note = memo
        self.parcel = parcel

        trs = tables[2].find_all('tr')
        for i, tr in enumerate(trs):
            if i != 0:
                tds = tr.find_all('td')

                time = getattr(tds[0], 'string', '')
                location = getattr(tds[1], 'string', '')
                phone = getattr(tds[2], 'string', '')
                status = getattr(tds[3], 'string', '')

                track = Track()
                track.time = time
                track.location = location
                track.status = status
                track.phone1 = phone
                self.add_track(track)
