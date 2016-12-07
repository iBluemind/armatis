# -*- coding: utf-8 -*-


from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class EMSParser(Parser):
    def __init__(self, invoice_number):
        super(EMSParser, self).__init__(invoice_number)
        parser_request = ParserRequest(url='http://trace.epost.go.kr/xtts/servlet/kpl.tts.common.svl.SttSVL?' \
                             'target_command=kpl.tts.tt.epost.cmd.RetrieveOrderEpostPoEmsKorCMD' \
                             '&JspURI=/xtts/tt/epost/ems' \
                             '/EmsSearchResult.jsp&POST_CODE=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser, response):
        div = parser.find('div', {'class': 'sub_emspop_table'})
        table = div.find('table')
        cols = table.find('thead').find('tr').find_all('th')
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            tds = row.find_all('td')

            time = getattr(tds[0], 'string', '')
            location = getattr(tds[2], 'string', '')
            status = getattr(tds[1], 'string', '')

            track = Track()
            track.location = location
            track.status = status
            track.time = time
            self.add_track(track)

