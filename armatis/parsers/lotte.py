# -*- coding: utf-8 -*-

from armatis.models import Parcel, Track
from armatis.parser import Parser


class LotteParser(Parser):
    def __init__(self, invoice_number, config):
        super(LotteParser, self).__init__(invoice_number, config)
        self.requests = [
            {
                'url': 'https://www.lotteglogis.com/home/personal/inquiry/track',
                'method': 'POST',
                'body': ('InvNo=%s&action=processInvoiceSubmit' % self.invoice_number).encode('utf-8'),
                'header': {'Content-Type': 'application/x-www-form-urlencoded'}
            },
            {
                'url': 'https://www.lotteglogis.com/home/personal/inquiry/track',
                'method': 'POST',
                'body': 'action=processInvoiceLinkSubmit'.encode('utf-8'),
                'header': {'Content-Type': 'application/x-www-form-urlencoded'}
            }
        ]

    def parse(self, parser):
        tr = parser.find('tr', {'class': 'bot'})
        tds = tr.find_all('td')
        address = tds[2].get_text(strip=True)

        parcel = Parcel()
        parcel.address = address
        self.parcel = parcel

        tables = parser.find_all('table', {'class': 'table_02'})
        trs = tables[1].find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 0:
                time = '%s %s' % (getattr(tds[0], 'string', ''), getattr(tds[1], 'string', ''))
                location = getattr(tds[2].a, 'string', '') or getattr(tds[2], 'string', '')
                status = getattr(tds[3].p, 'string', '')

                track = Track()
                track.time = time
                track.location = location
                track.status = status
                self.add_track(track)
