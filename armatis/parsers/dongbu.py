# -*- coding: utf-8 -*-


from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class DongbuParser(Parser):
    def __init__(self, invoice_number):
        super(DongbuParser, self).__init__(invoice_number)
        parser_request = ParserRequest(url='http://www.dongbups.com/newHtml/delivery/' \
                             'dvsearch_View.jsp?item_no=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser, response):
        tables = parser.find_all('table', {'class': 'dv_list'})

        basic_table = tables[0]
        trs = basic_table.find_all('tr')
        sender = getattr(trs[1].find_all('td')[0], 'string', '')
        receiver = getattr(trs[1].find_all('td')[1], 'string', '')

        parcel = Parcel()
        parcel.sender = sender
        parcel.receiver = receiver
        self.parcel = parcel

        track_table = tables[1]
        trs = track_table.find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 0:
                time = getattr(tds[0], 'string', '') + ' ' + getattr(tds[1], 'string', '')
                location = getattr(tds[2], 'string', '').split('/')[0]
                status = getattr(tds[3], 'string', '')
                phone = getattr(tds[2], 'string', '').split('/')[1]

                track = Track()
                track.time = time
                track.location = location
                track.status = status
                track.phone1 = ''.join(phone.split())
                self.add_track(track)

