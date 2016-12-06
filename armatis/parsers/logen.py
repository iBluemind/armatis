# -*- coding: utf-8 -*-


import re
from bs4 import BeautifulSoup
from armatis.models import Parcel, Track
from armatis.parser import Parser, ParserRequest


class LogenParser(Parser):
    def __init__(self, invoice_number):
        super(LogenParser, self).__init__(invoice_number)
        parser_request = ParserRequest()
        parser_request.url = 'http://www.ilogen.com/homeshopping/stracker_trace_xml.asp?' \
                             'invoice=%s' % self.invoice_number
        self.parser_request = parser_request

    def parser(self, doc):
        return BeautifulSoup(doc, 'html5lib')

    def parse(self, parser, response):
        response = response.decode('ms949', 'ignore')
        tracking_info = parser.find('tracking_info')

        sender_name = getattr(tracking_info.find('sender_name'), 'string', '')
        receiver_name = getattr(tracking_info.find('reciver_name'), 'string', '')
        receiver_addr = getattr(tracking_info.find('reciver_addr'), 'string', '')
        item_name = getattr(tracking_info.find('item_name'), 'string', '')
        if sender_name != None:
            sender_name = re.sub('[\[CDATA\]]', '', sender_name)
        if receiver_name != None:
            receiver_name = re.sub('[\[CDATA\]]', '', receiver_name)
        if receiver_addr != None:
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
            track.status = trans_kind
            track.location = trans_where
            track.phone1 = trans_telno
            self.add_track(track)


class GTXParser(LogenParser):
    def __init__(self, invoice_number):
        super(GTXParser, self).__init__(invoice_number)
        parser_request = ParserRequest()
        parser_request.url = 'http://www.gtxlogis.co.kr/tracking/' \
                             'tracking_xml.asp?invoice=%s' % self.invoice_number
        self.parser_request = parser_request


