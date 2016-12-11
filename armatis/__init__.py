# -*- coding: utf-8 -*-

"""
Armatis

Armatis parses the website or web API response of
Korean parcel delivery service company for tracking the parcel.

https://github.com/iBluemind/armatis
"""

from armatis.models import Company
from armatis.parser import ParserManager, Parser
from armatis.constants import TRACKING_RESULT_COMPANY

__author__ = 'Han Manjong (han@manjong.org)'
__version__ = '1.0.2'
__copyright__ = 'Copyright (c) 2016 Han Manjong'
__license__ = 'BSD'


class Armatis(object):
    def __init__(self, company_code=None, invoice_number=None):
        self.company_code = company_code
        self.invoice_number = invoice_number

        self.parser_manager = ParserManager()

        def register_parsers():
            from armatis.parsers.d2d import DoorToDoorParser, CVSNetParser
            self.parser_manager.register_parser(Company('CJ대한통운', 'cj', 10, '1588-1255'),
                                                DoorToDoorParser)
            self.parser_manager.register_parser(Company('CVSNet편의점택배', 'cvs', 10, '1577-1287'),
                                                CVSNetParser)
            from armatis.parsers.ems import EMSParser
            self.parser_manager.register_parser(Company('EMS', 'ems', 13, '1588-1300'),
                                                EMSParser)
            from armatis.parsers.epost import EPostParser
            self.parser_manager.register_parser(Company('우체국택배', 'epost', 13, '1588-1300'),
                                                EPostParser)
            from armatis.parsers.hanjin import HanjinParser
            self.parser_manager.register_parser(Company('한진택배', 'hanjin', 12, '1588-0011'),
                                                HanjinParser)
            from armatis.parsers.hapdong import HapdongParser
            self.parser_manager.register_parser(Company('합동택배', 'hapdong', 12, '080-873-2178'),
                                                HapdongParser)
            from armatis.parsers.hyundai import HyundaiParser
            self.parser_manager.register_parser(Company('현대택배', 'hyundai', 12, '1588-2121'),
                                                HyundaiParser)
            from armatis.parsers.kgb import KGBParser
            self.parser_manager.register_parser(Company('KGB택배', 'kgb', 10, '1588-4577'),
                                                KGBParser)
            from armatis.parsers.logen import LogenParser, GTXParser
            self.parser_manager.register_parser(Company('로젠택배', 'logen', 11, '1588-9988'),
                                                LogenParser)
            self.parser_manager.register_parser(Company('GTX로지스', 'gtx', 12, '1588-1756'),
                                                GTXParser)
            from armatis.parsers.kg_logis import KGLogisParser
            self.parser_manager.register_parser(Company('KG로지스', 'kglogis', 12, '1588-0123'),
                                                KGLogisParser)

        # Register the bundle parsers
        register_parsers()

        if self.company_code is not None and \
                self.invoice_number is not None:
            self._company, self._parser = self.parser(self.company_code,
                                                      self.invoice_number)

    def parser(self, company_code, invoice_number):
        """
        Get the parser for specific company

        :param str company_code: The company to find the parcel
        :param int invoice_number: The invoice number to find the parcel
        :return: The parser of the company
        """
        company, parser_cls = self.parser_manager[company_code]
        return company, parser_cls(invoice_number)

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
        track_result[TRACKING_RESULT_COMPANY] = {
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
