# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class KGBParser(Parser):
    def __init__(self, invoice_number, config):
        super(KGBParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://www.kgbls.co.kr/auction/?number=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        div = parser.find('div', {'class': 'myatable03 mts'})
        basic_table = div.find('table')
        tds = basic_table.find_all('td')

        sender_name = getattr(tds[0], 'string', '')
        address = getattr(tds[1], 'string', '')

        parcel = Parcel()
        parcel.sender = sender_name
        parcel.address = address
        self.parcel = parcel

        div2 = parser.find_all('div', {'class': 'myatable03 mtxxs'})[1]
        track_table = div2.find('table')
        rows = track_table.find_all('tr')

        for row in rows:
            tds = row.find_all('td')
            if len(tds) > 0:
                time = getattr(tds[0], 'string', '')
                status = getattr(tds[3], 'string', '')
                location = getattr(tds[1], 'string', '')
                phone = '%s %s' % (getattr(tds[4], 'string', ''),
                                   getattr(tds[2], 'string', ''))

                track = Track()
                track.time = time
                track.status = status
                track.location = location
                track.phone1 = phone
                self.add_track(track)
