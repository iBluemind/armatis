# -*- coding: utf-8 -*-

from armatis.models import Parcel, Track
from armatis.parser import Parser, ParserRequest


class DoorToDoorParser(Parser):
    def __init__(self, invoice_number, config):
        super(DoorToDoorParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://www.doortodoor.co.kr/tracking/jsp/cmn/Tracking_new.jsp?' \
                                           'QueryType=3&pOrderNo=&pTelNo=&pFromDate=&pToDate=&pCustId=&' \
                                           'pageno=1&rcv_cnt=10&pTdNo=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        tables = parser.find_all('tbody')
        cols = parser.find('thead').find('tr').find_all('th')

        trs = tables[0].find_all('tr')
        customer_infos = []
        for tr in trs:
            ths = tr.find_all('th')
            tds = tr.find_all('td')

            for index, th in enumerate(ths):
                td = tds[index].get_text(strip=True)

                if th != '':
                    customer_infos.append(td)

        parcel = Parcel()
        parcel.sender = customer_infos[1]
        parcel.receiver = customer_infos[4]
        parcel.address = customer_infos[6]
        parcel.note = customer_infos[7]
        self.parcel = parcel

        trs = tables[1].find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')

            location = getattr(tds[0], 'get_text', '')(strip=True)
            phone1 = getattr(tds[1], 'get_text', '')(strip=True)
            phone2 = getattr(tds[6], 'get_text', '')(strip=True)
            status = getattr(tds[2], 'get_text', '')(strip=True)
            time = getattr(tds[3], 'get_text', '')(strip=True)

            track = Track()
            track.location = location
            track.phone1 = phone1
            track.phone2 = phone2
            track.status = status
            track.time = time
            self.add_track(track)


class CVSNetParser(DoorToDoorParser):
    def __init__(self, invoice_number, config):
        super(CVSNetParser, self).__init__(invoice_number, config)
