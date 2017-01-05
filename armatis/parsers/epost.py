# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class EPostParser(Parser):
    def __init__(self, invoice_number, config):
        super(EPostParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(method='POST',
                                       header={'Content-Type': 'application/x-www-form-urlencoded'},
                                       url='https://service.epost.go.kr/'
                                           'trace.RetrieveDomRigiTraceList.comm',
                                       body=('sid1=%s' % self.invoice_number).encode('utf-8'))
        self.add_request(parser_request)

    def parse(self, parser):
        basic_table = parser.find_all('table', {'class': 'table_col'})[0]
        tds = basic_table.find_all('td')

        sender = tds[0]
        receiver = tds[1]
        note = tds[2]

        parcel = Parcel()
        parcel.sender = sender
        parcel.receiver = receiver
        parcel.note = note
        self.parcel = parcel

        track_table = parser.find_all('table', {'class': 'table_col'})[1]
        trs = track_table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 0:
                time = '%s %s' % (getattr(tds[0], 'string', ''), getattr(tds[1], 'string', ''))
                location = getattr(tds[2], 'string', '')
                status = getattr(tds[3], 'string', '')

                track = Track()
                track.time = time
                track.location = location
                track.status = status
                self.add_track(track)
