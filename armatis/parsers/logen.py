# -*- coding: utf-8 -*-

import re
from armatis.models import Parcel, Track
from armatis.parser import Parser, ParserRequest


class LogenParser(Parser):
    def __init__(self, invoice_number, config):
        config['RESPONSE_ENCODING'] = 'cp949'
        super(LogenParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest(url='http://www.ilogen.com/homeshopping/stracker_trace_xml.asp?' \
                                           'invoice=%s' % self.invoice_number)
        self.add_request(parser_request)

    def parse(self, parser):
        tracking_info = parser.find('tracking_info')

        sender_name = getattr(tracking_info.find('sender_name'), 'string', '')
        receiver_name = getattr(tracking_info.find('reciver_name'), 'string', '')
        receiver_addr = getattr(tracking_info.find('reciver_addr'), 'string', '')
        item_name = getattr(tracking_info.find('item_name'), 'string', '')
        if sender_name is not None:
            sender_name = re.sub('[\[CDATA\]]', '', sender_name)
        if receiver_name is not None:
            receiver_name = re.sub('[\[CDATA\]]', '', receiver_name)
        if receiver_addr is not None:
            receiver_addr = re.sub('[\[CDATA\]]', '', receiver_addr)

        parcel = Parcel()
        parcel.receiver = receiver_name
        parcel.sender = sender_name
        parcel.address = receiver_addr
        parcel.note = item_name
        self.parcel = parcel

        list_tracking_details = tracking_info.find_all('tracking_details')
        for tracking_details in list_tracking_details:
            trans_time = getattr(tracking_details.find('trans_time'), 'string', '')
            trans_kind = getattr(tracking_details.find('trans_kind'), 'string', '')
            trans_where = getattr(tracking_details.find('trans_where'), 'string', '')
            trans_telno = getattr(tracking_details.find('trans_telno'), 'string', '')

            track = Track()
            track.time = trans_time
            track.status = trans_kind
            track.location = trans_where
            track.phone1 = trans_telno
            self.add_track(track)


class GTXParser(LogenParser):
    def __init__(self, invoice_number, config):
        super(GTXParser, self).__init__(invoice_number, config)
        parser_request = ParserRequest('http://www.gtxlogis.co.kr/tracking/' \
                                       'tracking_xml.asp?invoice=%s' % self.invoice_number)
        self.add_request(parser_request)
        self.parser_request = parser_request
