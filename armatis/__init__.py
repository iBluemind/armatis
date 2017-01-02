# -*- coding: utf-8 -*-

"""
Armatis

Armatis parses the website or web API response of
Korean parcel delivery service company for tracking the parcel.

https://github.com/iBluemind/armatis
"""

from armatis.models import Company
from armatis.parser import ParserManager, Parser

__author__ = 'Han Manjong (han@manjong.org)'
__version__ = '1.1.0'
__copyright__ = 'Copyright (c) 2016 Han Manjong'
__license__ = 'BSD'


class Armatis(object):

    default_config = {
        'USER_AGENT_STRING': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'MULTIPLE_REQUEST_PERIOD': 2,
        'INVOICE_NUMBER_VALIDATION': False,
    }

    def __init__(self, company_code=None, invoice_number=None, *args, **kwargs):
        self.company_code = company_code
        self.invoice_number = invoice_number
        self.config = self._make_config(*args) if len(args) > 0 else \
            self._make_config(**kwargs)
        self.parser_manager = ParserManager()

        def register_parsers():
            from armatis.parsers.d2d import DoorToDoorParser, CVSNetParser
            self.parser_manager.register_parser(Company('CJ대한통운', 'cj', '1588-1255', [10, 12]),
                                                DoorToDoorParser)
            self.parser_manager.register_parser(Company('CVSNet편의점택배', 'cvs', '1577-1287', [10]),
                                                CVSNetParser)
            from armatis.parsers.ems import EMSParser
            self.parser_manager.register_parser(Company('EMS', 'ems', '1588-1300', [13]),
                                                EMSParser)
            from armatis.parsers.epost import EPostParser
            self.parser_manager.register_parser(Company('우체국택배', 'epost', '1588-1300', [13]),
                                                EPostParser)
            from armatis.parsers.hanjin import HanjinParser
            self.parser_manager.register_parser(Company('한진택배', 'hanjin', '1588-0011', [9, 10, 12]),
                                                HanjinParser)
            from armatis.parsers.hapdong import HapdongParser
            self.parser_manager.register_parser(Company('합동택배', 'hapdong', '080-873-2178', [12]),
                                                HapdongParser)
            from armatis.parsers.lotte import LotteParser
            self.parser_manager.register_parser(Company('롯데택배', 'lotte', '1588-2121', [10, 12, 13]),
                                                LotteParser)
            from armatis.parsers.kgb import KGBParser
            self.parser_manager.register_parser(Company('KGB택배', 'kgb', '1588-4577', [10]),
                                                KGBParser)
            from armatis.parsers.logen import LogenParser, GTXParser
            self.parser_manager.register_parser(Company('로젠택배', 'logen', '1588-9988', [11]),
                                                LogenParser)
            self.parser_manager.register_parser(Company('GTX로지스', 'gtx', '1588-1756', [11, 12]),
                                                GTXParser)
            from armatis.parsers.kg_logis import KGLogisParser
            self.parser_manager.register_parser(Company('KG로지스', 'kglogis', '1588-0123', [10, 12]),
                                                KGLogisParser)

        # Register the bundle parsers
        register_parsers()

        if self.company_code is not None and \
                self.invoice_number is not None:
            self._company, self._parser = self.parser(self.company_code,
                                                      self.invoice_number)

    def _make_config(self, user_agent=None, period=None, validation=None):
        config = self.default_config
        if user_agent:
            config['USER_AGENT_STRING'] = user_agent
        if period:
            config['MULTIPLE_REQUEST_PERIOD'] = period
        if validation:
            config['INVOICE_NUMBER_VALIDATION'] = validation
        return config

    def parser(self, company_code, invoice_number):
        """
        Get the parser for specific company

        :param str company_code: The company to find the parcel
        :param int invoice_number: The invoice number to find the parcel
        :param bool validation: Check the invoice number is valid
        :return: The parser of the company
        """
        company, parser_cls = self.parser_manager[company_code]
        if self.config['INVOICE_NUMBER_VALIDATION'] and len(company.digit) > 0:
            if len(str(invoice_number)) not in company.digit:
                raise ValueError('The invoice number is not valid!')
        return company, parser_cls(invoice_number, self.config)

    def supported_companies(self):
        """
        Registered parsers and companies

        :return: The list of company's name and company's parser code
        :rtype: dict
        """
        return list({'name': k.name, 'code': k.code} for k, _ in self.parser_manager)

    def find(self, company_code=None, invoice_number=None):
        """
        Track the parcel

        :param str company_code: The company's code to find the parcel
        :param int invoice_number: The invoice number to find the parcel
        :return: The result of the tracking parcel
        :rtype: dict
        """
        if not hasattr(self, '_parser'):
            if self.company_code is None:
                raise ValueError('The company_code must be set first.')
            if self.invoice_number is None:
                raise ValueError('The invoice_number must be set first.')
            self._company, self._parser = self.parser(self.company_code,
                                                      self.invoice_number)
        track_result = self._parser.find()
        track_result['company'] = {
            'name': self._company.name,
            'contact': self._company.phone
        }
        return track_result

    def last_result(self):
        """
        Return the most recent tracking result

        :return: The most recent tracking result
        :rtype: dict
        """
        return self._parser.result()
