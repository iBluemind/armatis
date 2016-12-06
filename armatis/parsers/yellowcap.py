# -*- coding: utf-8 -*-


from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class KGYellowCapParser(Parser):
    def __init__(self, invoice_number):
        super(KGYellowCapParser, self).__init__(invoice_number)
        parser_request = ParserRequest()
        parser_request.url = 'https://www.kgyellowcap.co.kr/delivery/waybill.html?mode=bill'
        parser_request.body = 'delivery=%s' % self.invoice_number
        self.parser_request = parser_request

    def parse(self, parser, response):
        basicTable = parser.find('table', {'class': 'view'})
        ths = basicTable.find_all('th')
        tds = basicTable.find_all('td')

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

        trackTable = parser.find('table', {'class': 'list'})
        cols = trackTable.find('thead').find('tr').find_all('th')
        rows = trackTable.find('tbody').find_all('tr')

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

