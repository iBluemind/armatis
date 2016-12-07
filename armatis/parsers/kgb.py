# -*- coding: utf-8 -*-


from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class KGBParser(Parser):
    def __init__(self, invoice_number):
        super(KGBParser, self).__init__(invoice_number)
        parser_request = ParserRequest(url='http://www.kgbls.co.kr/auction/?number=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser, response):
        basic_table = parser.find('table', {'class': 'view'})
        ths = basic_table.find_all('th')
        tds = basic_table.find_all('td')

        sender_name = getattr(tds[1], 'string', '')
        memo = getattr(tds[2], 'string', '')
        receiver_name = getattr(tds[3], 'string', '')
        address = getattr(tds[5], 'string', '')

        parcel = Parcel()
        parcel.sender = sender_name
        parcel.receiver = receiver_name
        parcel.address = address
        parcel.note = memo
        self.parcel = parcel

        track_table = parser.find('table', {'class': 'list'})
        cols = track_table.find('thead').find('tr').find_all('th')
        rows = track_table.find('tbody').find_all('tr')

        for row in rows:
            tds = row.find_all('td')

            time = getattr(tds[0], 'string', '')
            status = getattr(tds[1], 'string', '')
            location = getattr(tds[2], 'string', '')
            phone = getattr(tds[3], 'string', '')

            track = Track()
            track.status = status
            track.location = location
            track.phone1 = phone
            self.add_track(track)

