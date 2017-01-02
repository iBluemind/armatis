# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class EMSParser(Parser):
    def __init__(self, invoice_number, config):
        super(EMSParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='https://service.epost.go.kr/trace.RetrieveEmsRigiTraceList.comm?' \
                                           'POST_CODE=%s&displayHeader=N' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        table = parser.find('table', {'class': 'table_col ma_b_5'})
        cols = table.find('thead').find('tr').find_all('th')
        rows = table.find('tbody').find_all('tr')

        self.parcel = Parcel()
        for row in rows:
            tds = row.find_all('td')

            time = getattr(tds[0].find('br'), 'next_sibling', '') or \
                   getattr(tds[1].find('br'), 'next_sibling', '')
            status = getattr(tds[2], 'string', '')

            track = Track()
            track.status = status
            track.time = time
            self.add_track(track)
