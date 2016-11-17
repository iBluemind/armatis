# -*- coding: utf-8 -*-


import urllib.request
import six
from abc import abstractmethod, ABCMeta
from contextlib import closing
from weakref import WeakValueDictionary
from bs4 import BeautifulSoup
from kparcel.constants import PARSER_REQUEST_HEADER_USER_AGENT, \
    PARSER_RESULT_PARCEL, PARSER_RESULT_TRACKS
from kparcel.models import Parcel, Company, Tracker


class Source(object):
    def __init__(self):
        self.tracker = Tracker()

    @property
    def tracks(self):
        return self.tracker.tracks

    @property
    def parcel(self):
        return self.__parcel

    @parcel.setter
    def parcel(self, parcel):
        if not isinstance(parcel, Parcel):
            raise TypeError('The parcel must be Parcel!')
        self.__parcel = parcel

    def add_track(self, new_track):
        self.tracker.add_track(new_track)


class ParserRequest(object):
    def __init__(self, url=None, body=None, header={}):
        # API endpoint
        self.url = url
        # The body content for HTTP request
        self.body = body
        # The header content for HTTP request
        self.header = header
        # Add an user agent of Internet Explorer
        self.header['User-Agent'] = PARSER_REQUEST_HEADER_USER_AGENT


@six.add_metaclass(ABCMeta)
class Parser(object):
    def __init__(self, invoice_number):
        self.source = Source()
        self.__invoice_number = invoice_number

    @property
    def invoice_number(self):
        return self.__invoice_number

    @property
    def parser_request(self):
        return self.__parser_request

    @parser_request.setter
    def parser_request(self, parser_request):
        """
        Provide the additional HTTP request information for browsing the API

        :param ParserRequest parser_request: The HTTP request information
        """
        if not isinstance(parser_request, ParserRequest):
            raise TypeError('The parser_request must be ParserRequest!')
        self.__parser_request = parser_request

    @property
    def parcel(self):
        return self.source.parcel

    @parcel.setter
    def parcel(self, parcel):
        """
        Store the information of the found parcel

        :param Parcel parcel: The information of the parcel
        """
        if not isinstance(parcel, Parcel):
            raise TypeError('The parcel must be Parcel!')
        self.source.parcel = parcel

    def _make_request(self):
        pr = self.parser_request
        return urllib.request.Request(pr.url, pr.body, pr.header)

    def fetch(self):
        """
        Browsing the API request and return the response
        :return: The response of the API request
        """
        request = self._make_request()
        with closing(urllib.request.urlopen(request)) as response:
            return response.read()

    @abstractmethod
    def parse(self, parser, response):
        """
        Parse the response of the API request

        :param parser: The module for parsing the response
        :param str response: The response of the API request
        """
        raise NotImplemented('Please implement parse()!')

    def parser(self, doc):
        """
        The module for parsing the response of the API request

        :param str doc: The response of the API request
        :return: The module for parsing the response
        """
        return BeautifulSoup(doc, 'lxml')


    def add_track(self, new_track):
        """
        Add the tracking status information

        :param Track new_track: The tracking status information
        """
        self.source.add_track(new_track)

    def result(self):
        """
        Get the found parcel tracking informations

        :return: The found parcel and tracking informations
        :rtype: dict
        """
        return {
            PARSER_RESULT_PARCEL: self.source.parcel,
            PARSER_RESULT_TRACKS: self.source.tracks
        }


class ParserManager(object):
    def __init__(self):
        self._parsers = WeakValueDictionary()

    def __getitem__(self, company_code):
        return self._parsers[company_code]

    def __iter__(self):
        for parser in self.parsers:
            yield parser

    def __len__(self):
        return len(self._parsers)

    @property
    def parsers(self):
        """
        Get the parsers registered

        :return: Registered parsers
        :rtype: list
        """
        return self._parsers.values()

    def parser(self, company_code, invoice_number):
        """
        Get the parser for specific company

        :param str company_code: The company to find the parcel
        :param int invoice_number: The invoice number to find the parcel
        :return: The parser of the company
        """
        return self._parsers[company_code](invoice_number)

    def supported_companies(self):
        """
        Registered parsers and companies

        :return: The list of company's code and parser object
        :rtype: dict
        """
        return dict((k, v) for k, v in self._parsers.items())

    def register_parser(self, company, new_parser):
        """
        Register the new parser

        :param Company company: The new company
        :param Parser new_parser: The new parser
        """
        if not isinstance(company, Company):
            raise TypeError('The company must be Company!')
        if not issubclass(new_parser, Parser):
            raise TypeError('The new_parser must be Parser!')
        self._parsers[company.code] = new_parser

