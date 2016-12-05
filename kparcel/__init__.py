# -*- coding: utf-8 -*-

"""
KParcel

KParcel parses the website or web API response of
Korean parcel delivery service company for tracking the parcel.

https://github.com/iBluemind/kparcel
"""

from kparcel.models import Company
from kparcel.parser import ParserManager, Parser

__author__ = 'Han Manjong (han@manjong.org)'
__version__ = '2.0.0'
__copyright__ = 'Copyright (c) 2016 Manjong Han'
__license__ = 'BSD'
__all__ = ['KParcel']


class KParcel(object):
    def __init__(self, company_code=None, invoice_number=None):
        self.company_code = company_code
        self.invoice_number = invoice_number

        self.parser_manager = ParserManager()
        def register_parsers():
            from kparcel.parsers.d2d import DoorToDoorParser, CVSNetParser
            self.parser_manager.register_parser(Company('CJ대한통운', 'cj', 10, '1588-1255'),
                                                DoorToDoorParser)
            self.parser_manager.register_parser(Company('CVSNet편의점택배', 'cvs', 10, '1577-1287'),
                                                CVSNetParser)
            from kparcel.parsers.dongbu import DongbuParser
            self.parser_manager.register_parser(Company('동부택배', 'dongbu', 12, '1588-8848'),
                                                DongbuParser)
            from kparcel.parsers.ems import EMSParser
            self.parser_manager.register_parser(Company('EMS', 'ems', 13, '1588-1300'),
                                                EMSParser)
            from kparcel.parsers.epost import EPostParser
            self.parser_manager.register_parser(Company('우체국택배', 'epost', 13, '1588-1300'),
                                                EPostParser)
            from kparcel.parsers.hanjin import HanjinParser
            self.parser_manager.register_parser(Company('한진택배', 'hanjin', 12, '1588-0011'),
                                                HanjinParser)
            from kparcel.parsers.hapdong import HapdongParser
            self.parser_manager.register_parser(Company('합동택배', 'hapdong', 12, '080-873-2178'),
                                                HapdongParser)
            from kparcel.parsers.hyundai import HyundaiParser
            self.parser_manager.register_parser(Company('현대택배', 'hyundai', 12, '1588-2121'),
                                                HyundaiParser)
            from kparcel.parsers.kgb import KGBParser
            self.parser_manager.register_parser(Company('KGB택배', 'kgb', 10, '1588-4577'),
                                                KGBParser)
            from kparcel.parsers.logen import LogenParser, GTXParser
            self.parser_manager.register_parser(Company('로젠택배', 'logen', 11, '1588-9988'),
                                                LogenParser)
            self.parser_manager.register_parser(Company('GTX로지스', 'gtx', 12, '1588-1756'),
                                                GTXParser)
            from kparcel.parsers.yellowcap import KGYellowCapParser
            self.parser_manager.register_parser(Company('KG옐로우캡', 'kgyellow', 11, '1588-0123'),
                                                KGYellowCapParser)

        # Register the bundle parsers
        register_parsers()

        if self.company_code is not None and \
                self.invoice_number is not None:
            self._parser = self.parser(self.company_code,
                                       self.invoice_number)

    def parser(self, company_code, invoice_number):
        """
        Get the parser for specific company

        :param str company_code: The company to find the parcel
        :param int invoice_number: The invoice number to find the parcel
        :return: The parser of the company
        """
        return self.parser_manager.parser(company_code, invoice_number)

    def supported_companies(self):
        """
        Registered parsers and companies

        :return: The list of company's name and company's parser code
        :rtype: dict
        """
        companies = self.parser_manager.supported_companies()
        return list({'name': k, 'code': v} for k, v in companies.items())

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
            self._parser = self.parser(self.company_code,
                                       self.invoice_number)
        response = self._parser.fetch()
        parser = self._parser.parser(response)
        self._parser.parse(parser, response)
        return self._parser.result()
