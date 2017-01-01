# -*- coding: utf-8 -*-

from armatis.models import Track, Parcel
from armatis.parser import Parser, ParserRequest


class KGLogisParser(Parser):
    def __init__(self, invoice_number, config):
        super(KGLogisParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='https://www.kglogis.co.kr/delivery/delivery_result.jsp',
                                       method='POST',
                                       body='item_no=%s' % self.invoice_number,
                                       header={'Content-Type': 'application/x-www-form-urlencoded'})
        self.add_request(parser_request)

    def parse(self, parser):
        basic_table = parser.find('table', {'class': 'i_table_01'})
        trs = basic_table.find_all('tr')

        sender = trs[0].find_all('td')[1].get_text()
        note = trs[1].find_all('td')[0].get_text()
        receiver = trs[1].find_all('td')[1].get_text()
        address = trs[3].find('td').get_text()

        parcel = Parcel()
        parcel.sender = sender
        parcel.receiver = receiver
        parcel.address = address
        parcel.note = note
        self.parcel = parcel

        track_table = parser.find('table', {'class': 'c_table_01'})
        trs = track_table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) == 5:
                time = '%s %s' % (
                    tds[0].find('span').get_text(),
                    tds[1].find('span').get_text(),
                )
                status = tds[2].find('span').get_text()
                location = tds[3].find('span').get_text()
                phone1 = tds[4].find('span').get_text()

                track = Track()
                track.time = time
                track.status = status
                track.location = location
                track.phone1 = phone1
                self.add_track(track)
